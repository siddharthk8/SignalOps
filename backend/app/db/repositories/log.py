from sqlalchemy.orm import Session

from app.db.models.log import Log
from app.schemas.log import JSONIncomingLog, LogsField


class LogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_logs(self, *, batch_id: int, logs: LogsField) -> None:
        data: list[Log] = []

        for log in logs:
            if isinstance(log, JSONIncomingLog):
                data.append(Log(batch_id=batch_id, **log.model_dump()))
            else:
                data.append(Log(batch_id=batch_id, message=log))

        self.db.add_all(data)
        self.db.flush()
