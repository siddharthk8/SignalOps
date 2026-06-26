from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.batch import Batch


class BatchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_and_get_batch(self, source_app_id: int) -> Batch:
        batch = Batch(source_app_id=source_app_id)
        self.db.add(batch)
        await self.db.flush()
        return batch

    async def get_total_batches(self, source_app_id: int) -> int:
        query = await self.db.execute(
            select(func.count())
            .select_from(Batch)
            .where(Batch.source_app_id == source_app_id)
        )
        result = query.scalar_one()
        return result or 0

    async def get_paginated_batches(
        self, source_app_id: int, skip: int, limit: int
    ) -> Sequence[Batch]:
        query = await self.db.execute(
            select(Batch)
            .options(selectinload(Batch.ai_analysis))
            .where(Batch.source_app_id == source_app_id)
            .order_by(Batch.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = query.scalars().all()
        return result
