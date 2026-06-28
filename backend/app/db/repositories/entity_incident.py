from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.entity_incident import EntityIncident


class EntityIncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, entity_id: int, incident_id: int):
        self.db.add(EntityIncident(entity_id=entity_id, incident_id=incident_id))
