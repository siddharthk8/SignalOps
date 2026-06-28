from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.event_signal import EventSignal


class EventSignalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, event_id: int, signal_id: int):
        self.db.add(EventSignal(event_id=event_id, signal_id=signal_id))

    async def filter_for_response(self, event_ids: set[int]):
        query = await self.db.execute(
            select(EventSignal).where(EventSignal.event_id.in_(event_ids))
        )
        result = query.scalars().all()
        return result
