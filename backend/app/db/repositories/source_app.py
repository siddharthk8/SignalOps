from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

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
        return await self.db.get(SourceApp, source_app_id)

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
