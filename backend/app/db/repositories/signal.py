from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal import Signal as ORMSignal
from app.schemas.signal import Signal


class SignalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_signals(
        self,
        *,
        signals: list[Signal],
    ) -> None:
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

            self.db.add(orm_signal)
        # self.db.flush() # Not required for now.
