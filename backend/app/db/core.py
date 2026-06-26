from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.database_url.get_secret_value(), pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=True
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as db_session:
        yield db_session


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
