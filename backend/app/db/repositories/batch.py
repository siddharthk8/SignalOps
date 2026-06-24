from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.batch import Batch


class BatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_and_get_batch(self, source_app_id: int) -> Batch:
        batch = Batch(source_app_id=source_app_id)
        self.db.add(batch)
        self.db.flush()
        return batch

    def get_total_batches(self, source_app_id: int) -> int:
        query = self.db.execute(
            select(func.count())
            .select_from(Batch)
            .where(Batch.source_app_id == source_app_id)
        ).scalar()
        return query or 0

    def get_paginated_batches(
        self, source_app_id: int, skip: int, limit: int
    ) -> Sequence[Batch]:
        return (
            self.db.execute(
                select(Batch)
                .where(Batch.source_app_id == source_app_id)
                .order_by(Batch.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )
