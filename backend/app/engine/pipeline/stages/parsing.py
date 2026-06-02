from sqlalchemy.orm import Session

from app.db.models.batch import Batch
from app.engine.parsing.registery import PARSER_REGISTRY
from app.enums.common import SourceAppType
from app.schemas.event import SemanticEvent
from app.schemas.log import LogField, LogsField


class ParsingStage:
    def __init__(self, db: Session, batch_orm: Batch):
        self.db = db
        self.batch_orm = batch_orm

    async def run(
        self, logs: LogsField, source_app: SourceAppType
    ) -> tuple[list[SemanticEvent], list[tuple[int, LogField]]]:

        parser = PARSER_REGISTRY[source_app]
        resolved_events: list[SemanticEvent] = []
        unresolved_logs: list[tuple[int, LogField]] = []

        for i, log in enumerate(logs):
            event = parser.parse(log, i)
            if event:
                resolved_events.append(event)
            else:
                unresolved_logs.append((i, log))

        return resolved_events, unresolved_logs

    def merge_ai_events(
        self,
        events: list[SemanticEvent],
        ai_events: list[SemanticEvent],
        unresolved_logs: list[tuple[int, LogField]],
    ) -> None:

        positions = [p for p, _ in unresolved_logs]
        for i in range(len(ai_events)):
            event = ai_events[i]
            event.sequence = positions[i]
            events.append(event)

        events.sort(key=lambda e: e.sequence)
