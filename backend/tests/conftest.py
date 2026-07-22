import asyncio
import sys

# Fix for Windows compatibility with async PostgreSQL (psycopg) and Alembic
# Forces SelectorEventLoop instead of ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os

os.environ["DB_DRIVER"] = "postgresql+psycopg"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "testdb"
os.environ["DB_USERNAME"] = "testuser"
os.environ["DB_PASSWORD"] = "testpass85"

os.environ["SECRET_KEY"] = "dummy-secret-key-for-testing-only"
os.environ["BEDROCK_MODEL_ID"] = "testing-model"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
os.environ["S3_BUCKET_REGION"] = "ap-south-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["MAIL_FROM"] = "test.sender@example.com"
os.environ["TESTING"] = "true"

from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any
from unittest.mock import Mock, patch

import boto3
import pytest
from httpx import ASGITransport, AsyncClient
from moto import mock_aws
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.core import Base, get_db
from main import app

pytest_plugins = ["anyio"]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def test_engine():
    database_url = URL.create(
        drivername=os.environ["DB_DRIVER"],
        username=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    return create_async_engine(
        database_url,
        poolclass=NullPool,
    )


@pytest.fixture(scope="session")
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session(
    test_engine,
    setup_database,
) -> AsyncGenerator[AsyncSession]:
    # NOTE:
    # Each test runs inside a transaction that is rolled back after completion,
    # so table data is isolated between tests.
    #
    # PostgreSQL sequences (SERIAL/IDENTITY), however, are NOT transactional.
    # Auto-increment IDs continue to increase across tests even though rows are
    # rolled back. Tests must therefore never assume IDs start at 1; instead,
    # obtain generated IDs from the API response or query the database.
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


@pytest.fixture
def mocked_aws():
    with mock_aws():
        s3 = boto3.client("s3", region_name=os.environ["S3_BUCKET_REGION"])
        s3.create_bucket(
            Bucket=os.environ["S3_BUCKET_NAME"],
            CreateBucketConfiguration={
                "LocationConstraint": os.environ["S3_BUCKET_REGION"]
            },
        )
        yield s3


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with (
        AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",  # Placeholder URL. ASGITransport routes requests directly to the FastAPI app, so the host is ignored.
        ) as async_client
    ):
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
async def mocked_bedrock_client():
    client = Mock()

    with patch(
        "app.engine.pipeline.stages.ai.boto3.client",
        return_value=client,
    ):
        yield client


@dataclass
class TestUser:
    first_name: str = "First"
    last_name: str = "Last"
    email: str = "test@example.com"
    password: str = "String@123"


DEFAULT_USER = TestUser()


async def create_test_user(
    client: AsyncClient,
    first_name: str = DEFAULT_USER.first_name,
    last_name: str = DEFAULT_USER.last_name,
    email: str = DEFAULT_USER.email,
    password: str = DEFAULT_USER.password,
) -> dict[str, Any]:
    response = await client.post(
        "/api/v1/users",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 201, f"Failed to create user: {response.text}"
    return response.json()


async def login_user(
    client: AsyncClient,
    email: str = DEFAULT_USER.email,
    password: str = DEFAULT_USER.password,
) -> tuple[str, str]:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == 200, f"Failed to login: {response.text}"
    return response.json()["access_token"], response.json()["refresh_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# other
@dataclass
class TestSourceApp:
    name: str = "sample-app"
    app_type: str = "auth-app"


DEFAULT_SOURCE_APP = TestSourceApp()

# Constants
NORMALIZE_LOGS_RESPONSE = {
    "output": {
        "message": {
            "content": [
                {
                    "toolUse": {
                        "input": {
                            "events": [
                                {
                                    "severity": "low",
                                    "event_type": "other",
                                    "confidence": 0.8,
                                    "id": 4,
                                }
                            ]
                        },
                    }
                }
            ],
        }
    }
}

ANALYZE_INCIDENTS_RESPONSE = {
    "output": {
        "message": {
            "content": [
                {
                    "toolUse": {
                        "input": {
                            "analyses": [
                                {
                                    "summary": "An excessive number of authentication failures originating from IP address 192.168.1.10 within a 5-minute window between 09:00 UTC and 09:01 UTC on June 28, 2026, triggered a high-severity security alert.",
                                    "severity": "high",
                                    "incident_type": "account_security",
                                    "incident_index": 0,
                                    "confidence": 0.9,
                                    "business_impact": [
                                        "Potential account compromise if the failed attempts were malicious.",
                                        "Possible unauthorized access attempts.",
                                    ],
                                    "recommendations": [
                                        "Investigate the source IP address 192.168.1.10 to determine the nature of the failed login attempts.",
                                        "Review authentication logs for further details on the failed attempts (e.g., attempted passwords).",
                                        "Consider implementing rate limiting or account lockout policies for suspicious IP addresses.",
                                    ],
                                    "root_cause": "Excessive authentication failures from a single IP address likely indicate a brute-force attack or other malicious activity attempting to gain unauthorized access to user accounts.",
                                }
                            ]
                        },
                    }
                }
            ],
        }
    }
}
