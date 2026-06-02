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
