from sqlalchemy.orm import Session

from app.db.models.log import Log
from app.schemas.log import JSONIncomingLog, LogsField, PersistedLog


class LogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    @staticmethod
    def _return_persisted_logs(data: list[Log], logs: LogsField) -> list[PersistedLog]:
        persisted_logs: list[PersistedLog] = []

        for i, log in enumerate(logs):
            if isinstance(log, JSONIncomingLog):
                persisted_logs.append(
                    PersistedLog(id=data[i].id, log_format="json", **log.model_dump())
                )
            else:
                persisted_logs.append(
                    PersistedLog(id=data[i].id, log_format="string", message=log)
                )

        return persisted_logs

    def save_logs(self, *, batch_id: int, logs: LogsField) -> list[PersistedLog]:
        data: list[Log] = []

        for log in logs:
            if isinstance(log, JSONIncomingLog):
                data.append(Log(batch_id=batch_id, **log.model_dump()))
            else:
                data.append(Log(batch_id=batch_id, message=log))

        self.db.add_all(data)
        self.db.flush()

        return self._return_persisted_logs(data, logs)
