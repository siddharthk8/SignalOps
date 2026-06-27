import asyncio
import sys
from dataclasses import dataclass

# Fix for Windows compatibility with async PostgreSQL (psycopg) and Alembic
# Forces SelectorEventLoop instead of ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from collections.abc import AsyncGenerator
from typing import Any
from uuid import UUID

os.environ["SECRET_KEY"] = "dummy-secret-key-for-testing-only"
os.environ["DATABASE_URL"] = "postgresql+psycopg://testuser:testpass85@localhost/testdb"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
os.environ["S3_BUCKET_REGION"] = "ap-south-1"


import boto3
import pytest
from httpx import ASGITransport, AsyncClient
from moto import mock_aws
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
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        poolclass=NullPool,
    )
    return engine


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
async def client(
    db_session: AsyncSession,
    mocked_aws,
) -> AsyncGenerator[AsyncClient]:

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


@dataclass
class TestUser:
    first_name: str = "First"
    last_name: str = "Last"
    email: str = "test@example.com"
    password: str = "String123"


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
    id: UUID,
    password: str = "String123",
) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": id,
            "password": password,
        },
    )
    assert response.status_code == 200, f"Failed to login: {response.text}"
    return response.json()["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
