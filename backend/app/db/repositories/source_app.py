from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.source_app import SourceApp
from app.enums.common import SourceAppType


class SourceAppRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_source_app(
        self, *, user_id: UUID, name: str, app_type: SourceAppType
    ) -> SourceApp:
        source_app_orm = SourceApp(
            user_id=user_id,
            name=name,
            app_type=app_type.value,
        )
        self.db.add(source_app_orm)
        await self.db.flush()
        return source_app_orm

    async def get_by_id(self, source_app_id: int) -> SourceApp | None:
        result = await self.db.execute(
            select(SourceApp).where(SourceApp.id == source_app_id)
        )
        return result.scalar_one_or_none()

    async def get_by_access_key(self, access_key: str) -> SourceApp | None:
        result = await self.db.execute(
            select(SourceApp)
            .options(selectinload(SourceApp.user))
            .where(SourceApp.access_key == access_key)
        )
        return result.scalar_one_or_none()

    async def get_total_source_apps(self, user_id: UUID) -> int:
        query = await self.db.execute(
            select(func.count())
            .select_from(SourceApp)
            .where(SourceApp.user_id == user_id)
        )
        result = query.scalar_one()
        return result or 0

    async def get_paginated_source_apps(
        self, user_id: UUID, skip: int, limit: int
    ) -> Sequence[SourceApp]:
        query = await self.db.execute(
            select(SourceApp)
            .where(SourceApp.user_id == user_id)
            .order_by(SourceApp.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = query.scalars().all()
        return result

    async def remove_source_app(self, source_app: SourceApp):
        await self.db.delete(source_app)

    async def get_count_by_user(self, user_id: UUID) -> int:
        query = await self.db.execute(
            select(func.count())
            .select_from(SourceApp)
            .where(SourceApp.user_id == user_id)
        )
        count = query.scalar()
        return count or 0

    async def update_source_app_access_token(
        self,
        access_key: str | None,
        secret_access_key_hash: str | None,
        source_app_id: int,
        user_id: UUID,
    ):
        await self.db.execute(
            update(SourceApp)
            .where(SourceApp.user_id == user_id, SourceApp.id == source_app_id)
            .values(
                access_key=access_key, secret_access_key_hash=secret_access_key_hash
            )
        )
