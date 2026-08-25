import asyncio
import sys

# Fix for Windows compatibility with async PostgreSQL (psycopg) and Alembic
# Forces SelectorEventLoop instead of ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os

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

from app.core.config import settings
from app.db.core import Base, get_db
from main import app

pytest_plugins = ["anyio"]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def env_values():
    return settings


@pytest.fixture(scope="session")
def test_engine():
    database_url = URL.create(
        drivername=settings.db_driver,
        username=settings.db_username.get_secret_value(),
        password=settings.db_password.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
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
        s3 = boto3.client("s3", region_name=settings.s3_region)
        s3.create_bucket(
            Bucket=settings.s3_bucket_name,
            CreateBucketConfiguration={"LocationConstraint": settings.s3_region},
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
                                    "summary": "An incident involving excessive authentication failures was detected from IP address 192.168.1.10. The event occurred within a 3-minute window between June 28, 2026, 09:00 UTC and June 28, 2026, 09:00 UTC, with 3 failed attempts.",
                                    "severity": "high",
                                    "incident_type": "account_security",
                                    "incident_index": 0,
                                    "confidence": 0.9,
                                    "business_impact": [
                                        "Potential account compromise if not addressed.",
                                        "Reputational damage due to security incidents.",
                                    ],
                                    "recommendations": [
                                        "Investigate the source IP address 192.168.1.10 to determine the user attempting the attacks.",
                                        "Implement rate limiting on authentication attempts for the affected user or IP address.",
                                        "Review logs for any associated user activity.",
                                    ],
                                    "root_cause": "Excessive authentication failures from a single IP address likely indicate a brute-force or credential stuffing attack. The specific user attempting the attacks is unknown based on the available data. The window of 3 minutes suggests a sustained attack attempt. The lack of entity data (user, email, etc.) makes it difficult to determine the scope of the issue.",
                                },
                                {
                                    "summary": "A brute-force attempt was detected from IP address 192.168.1.10. The event occurred within a 3-minute window between June 28, 2026, 09:00 UTC and June 28, 2026, 09:00 UTC, with 3 attempts.",
                                    "severity": "high",
                                    "incident_type": "account_security",
                                    "incident_index": 1,
                                    "confidence": 0.95,
                                    "business_impact": [
                                        "Potential account compromise if not addressed.",
                                        "Reputational damage due to security incidents.",
                                    ],
                                    "recommendations": [
                                        "Investigate the source IP address 192.168.1.10 to determine the user attempting the brute-force attack.",
                                        "Implement rate limiting on login attempts for the affected user or IP address.",
                                        "Review logs for any associated user activity.",
                                    ],
                                    "root_cause": "Multiple brute-force attempts detected from a single IP address. The event occurred within a 3-minute window. The lack of entity data (user, email, etc.) makes it difficult to determine the scope of the issue.",
                                },
                            ]
                        }
                    }
                }
            ]
        }
    }
}
