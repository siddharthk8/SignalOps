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
