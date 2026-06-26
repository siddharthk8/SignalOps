from collections.abc import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.event import Event
from app.db.repositories.entity import EntityRepository
from app.schemas.event import SemanticEvent


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter_for_response(self, batch_id: int) -> Sequence[Event]:
        query = await self.db.execute(
            select(Event)
            .options(selectinload(Event.entity), selectinload(Event.log))
            .where(Event.batch_id == batch_id)
        )
        result = query.scalars().all()
        return result

    async def save_signal_id(self, signal_id: int, event_ids: list[int]):
        await self.db.execute(
            update(Event).where(Event.id.in_(event_ids)).values(signal_id=signal_id)
        )

    async def save_events(
        self,
        *,
        batch_id: int,
        events: list[SemanticEvent],
    ) -> None:
        db_events: list[Event] = []
        entity_repo = EntityRepository(self.db)

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
                entity_orm = await entity_repo.save(event.entity)
                entity_id = entity_orm.id

            db_event = Event(
                batch_id=batch_id,
                entity_id=entity_id,
                **event_payload,
            )

            # storing id of entity
            event.entity.id = entity_id

            self.db.add(db_event)
            db_events.append(db_event)

        await self.db.flush()

        # store ids of events.
        for i, orm_event in enumerate(db_events):
            events[i].id = orm_event.id
