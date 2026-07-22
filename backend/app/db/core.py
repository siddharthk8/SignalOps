from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

database_url = URL.create(
    drivername=settings.db_driver,
    username=settings.db_username.get_secret_value(),
    password=settings.db_password.get_secret_value(),
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_async_engine(database_url, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=True
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as db_session:
        yield db_session


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
