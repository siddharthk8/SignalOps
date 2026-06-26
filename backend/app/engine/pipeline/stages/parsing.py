from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.batch import Batch
from app.db.repositories.event import EventRepository
from app.db.repositories.log import LogRepository
from app.engine.parsing.registery import PARSER_REGISTRY
from app.enums.common import SourceAppType
from app.schemas.event import SemanticEvent
from app.schemas.log import LogsField, PersistedLog


class ParsingStage:
    def __init__(self, db: AsyncSession, batch_orm: Batch):
        self.db = db
        self.batch_orm = batch_orm

        self.log_repo = LogRepository(db)
        self.event_repo = EventRepository(db)

    async def run(
        self, logs: LogsField, source_app: SourceAppType
    ) -> tuple[list[SemanticEvent], list[tuple[int, PersistedLog]]]:

        # save raw logs in db
        persisted_logs = await self.log_repo.save_logs(
            batch_id=self.batch_orm.id, logs=logs
        )

        parser = PARSER_REGISTRY[source_app]
        resolved_events: list[SemanticEvent] = []
        unresolved_logs: list[tuple[int, PersistedLog]] = []

        for i, log in enumerate(persisted_logs):
            event = parser.parse(log, i)
            if event:
                resolved_events.append(event)
            else:
                unresolved_logs.append((i, log))

        if len(unresolved_logs) == 0 and len(resolved_events) > 0:
            # save sementic events in db, if no unresolved_logs exists
            await self.event_repo.save_events(
                batch_id=self.batch_orm.id, events=resolved_events
            )

        return resolved_events, unresolved_logs

    async def merge_ai_events(
        self,
        events: list[SemanticEvent],
        ai_events: list[SemanticEvent],
        unresolved_logs: list[tuple[int, PersistedLog]],
    ) -> None:

        sequence = [s for s, _ in unresolved_logs]
        for i in range(len(ai_events)):
            event = ai_events[i]
            event.sequence = sequence[i]
            events.append(event)

        events.sort(key=lambda e: e.sequence)

        # save sementic events in db
        await self.event_repo.save_events(batch_id=self.batch_orm.id, events=events)
