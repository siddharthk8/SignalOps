from collections.abc import Sequence
from typing import cast

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal import Signal as ORMSignal
from app.db.repositories.event import EventRepository
from app.schemas.signal import Signal


class SignalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter_for_response(self, ids: set[int]) -> Sequence[ORMSignal]:
        query = await self.db.execute(select(ORMSignal).where(ORMSignal.id.in_(ids)))
        result = query.scalars().all()
        return result

    async def save_incident_id(self, incident_id: int, signal_ids: list[int]):
        await self.db.execute(
            update(ORMSignal)
            .where(ORMSignal.id.in_(signal_ids))
            .values(incident_id=incident_id)
        )

    async def save_signals(self, *, signals: list[Signal]) -> None:
        db_signals: list[ORMSignal] = []

        for signal in signals:
            signal_payload = signal.model_dump(
                exclude={"signal_type", "supporting_events", "entity", "metadata"}
            )
            signal_payload["signal_type"] = signal.signal_type.value
            if signal.entity:
                signal_payload["entity_id"] = signal.entity.id

            orm_signal = ORMSignal(
                **signal_payload,
            )

            db_signals.append(orm_signal)
            self.db.add(orm_signal)
        await self.db.flush()

        event_repo = EventRepository(self.db)

        for i, signal_orm in enumerate(db_signals):
            # store ids of signals.
            signals[i].id = signal_orm.id

            supporting_events = signals[i].supporting_events
            event_ids = [cast(int, e.id) for e in supporting_events]
            await event_repo.save_signal_id(signal_orm.id, event_ids)
