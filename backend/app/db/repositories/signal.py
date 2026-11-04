from collections.abc import Sequence
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal import Signal as ORMSignal
from app.db.repositories.event_signal import EventSignalRepository
from app.schemas.signal import Signal


class SignalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter_for_response(self, ids: set[int]) -> Sequence[ORMSignal]:
        query = await self.db.execute(select(ORMSignal).where(ORMSignal.id.in_(ids)))
        result = query.scalars().all()
        return result

    async def save(self, *, signals: list[Signal], batch_id: int) -> None:
        signal_models: list[ORMSignal] = []

        for signal in signals:
            signal_payload = signal.model_dump(
                exclude={"signal_type", "supporting_events", "entity", "metadata"}
            )
            signal_payload["signal_type"] = signal.signal_type.value
            if signal.entity:
                signal_payload["entity_id"] = signal.entity.id

            signal_payload["batch_id"] = batch_id
            signal_model = ORMSignal(**signal_payload)
            signal_models.append(signal_model)

            self.db.add(signal_model)

        # Flushed to get db ids in signal_models
        await self.db.flush()
        event_signal_repo = EventSignalRepository(self.db)

        for i, s_model in enumerate(signal_models):
            # store ids of signals.
            signals[i].id = s_model.id

            # mapping events with signals
            for event in signal.supporting_events:
                await event_signal_repo.save(cast(int, event.id), s_model.id)

        await self.db.flush()
