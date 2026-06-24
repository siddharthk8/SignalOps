from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.source_app import SourceApp
from app.enums.common import SourceAppType


class SourceAppRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_source_app(self, *, name: str, app_type: SourceAppType):
        self.db.add(
            SourceApp(
                name=name,
                app_type=app_type.value,
            )
        )
        self.db.flush()

    def get_by_id(self, source_app_id: int) -> SourceApp | None:
        return self.db.get(SourceApp, source_app_id)

    def get_total_source_apps(self, user_id: UUID) -> int:
        query = self.db.execute(
            select(func.count())
            .select_from(SourceApp)
            .where(SourceApp.user_id == user_id)
        ).scalar()
        return query or 0

    def get_paginated_source_apps(
        self, user_id: UUID, skip: int, limit: int
    ) -> Sequence[SourceApp]:
        return (
            self.db.execute(
                select(SourceApp)
                .where(SourceApp.user_id == user_id)
                .order_by(SourceApp.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )
