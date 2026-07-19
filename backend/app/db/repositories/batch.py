from collections.abc import Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.batch import Batch
from app.db.models.log import Log


class BatchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_and_get_batch(self, source_app_id: int) -> Batch:
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
    ) -> Sequence[Row[tuple[Batch, int]]]:
        query = await self.db.execute(
            select(
                Batch,
                func.count(Log.id).label("log_count"),
            )
            .outerjoin(Log, Log.batch_id == Batch.id)
            .options(selectinload(Batch.ai_analyses))
            .where(Batch.source_app_id == source_app_id)
            .group_by(Batch.id)
            .order_by(Batch.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = query.all()
        return result

    async def get(self, batch_id: int):
        query = await self.db.execute(
            select(Batch)
            .options(selectinload(Batch.source_app), selectinload(Batch.ai_analyses))
            .where(Batch.id == batch_id)
        )
        result = query.scalar_one_or_none()
        return result
