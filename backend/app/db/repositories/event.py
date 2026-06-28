from collections.abc import Sequence

from sqlalchemy import select
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

    async def save(
        self,
        *,
        batch_id: int,
        events: list[SemanticEvent],
    ) -> None:
        event_models: list[Event] = []
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
                entity_model = await entity_repo.save(event.entity)
                entity_id = entity_model.id

            event_model = Event(
                batch_id=batch_id,
                entity_id=entity_id,
                **event_payload,
            )

            # storing id of entity
            event.entity.id = entity_id

            self.db.add(event_model)
            event_models.append(event_model)

        await self.db.flush()

        # store ids of events.
        for i, e_model in enumerate(event_models):
            events[i].id = e_model.id
