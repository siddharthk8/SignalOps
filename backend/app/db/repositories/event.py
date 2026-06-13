from sqlalchemy.orm import Session

from app.db.models.entity import Entity
from app.db.models.event import Event
from app.schemas.event import SemanticEvent


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_events(
        self,
        *,
        batch_id: int,
        events: list[SemanticEvent],
    ) -> None:
        db_events: list[Event] = []

        for event in events:
            event_payload = event.model_dump(
                exclude={
                    "id",
                    "sequence",
                    "source_app",
                    "persisted_log",
                    "entity",
                    "metadata",
                }
            )
            event_payload["event_type"] = event.event_type.value
            event_payload["parsing_method"] = event.parsing_method.value
            event_payload["severity"] = event.severity.value
            event_payload["log_id"] = event.persisted_log.id

            entity_id = None

            if any(value is not None for _, value in event.entity):
                entity_payload = event.entity.model_dump(exclude={"id", "ip_address"})
                entity_payload["ip_address"] = str(event.entity.ip_address)

                entity = Entity(**entity_payload)
                self.db.add(entity)
                self.db.flush()
                entity_id = entity.id

            db_event = Event(
                batch_id=batch_id,
                entity_id=entity_id,
                **event_payload,
            )

            # storing id of entity
            event.entity.id = entity_id

            self.db.add(db_event)
            db_events.append(db_event)

        self.db.flush()

        # store ids of events.
        for i, orm_event in enumerate(db_events):
            events[i].id = orm_event.id
