from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.log import Log
from app.schemas.log import JSONIncomingLog, LogsField, PersistedLog


class LogRepository:
    def __init__(self, db: AsyncSession) -> None:
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

    async def save_logs(self, *, batch_id: int, logs: LogsField) -> list[PersistedLog]:
        data: list[Log] = []

        for log in logs:
            if isinstance(log, JSONIncomingLog):
                log_payload = log.model_dump(exclude={"ip_address"})
                if log.ip_address:
                    log_payload["ip_address"] = str(log.ip_address)

                data.append(Log(batch_id=batch_id, **log_payload))
            else:
                data.append(Log(batch_id=batch_id, message=log))

        self.db.add_all(data)
        await self.db.flush()

        return self._return_persisted_logs(data, logs)
