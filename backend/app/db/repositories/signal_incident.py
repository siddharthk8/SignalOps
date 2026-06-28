from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal_incident import SignalIncident


class SignalIncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, signal_id: int, incident_id: int):
        self.db.add(SignalIncident(signal_id=signal_id, incident_id=incident_id))

    async def filter_for_response(self, signal_ids: set[int]):
        query = await self.db.execute(
            select(SignalIncident).where(SignalIncident.signal_id.in_(signal_ids))
        )
        result = query.scalars().all()
        return result
