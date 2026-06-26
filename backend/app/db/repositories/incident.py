from collections.abc import Sequence
from typing import cast

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.incident import Incident as ORMIncident
from app.db.models.incident_entities import IncidentEntities
from app.db.repositories.signal import SignalRepository
from app.schemas.incident import Incident


class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter_for_response(self, ids: set[int]) -> Sequence[ORMIncident]:
        query = await self.db.execute(
            select(ORMIncident).where(ORMIncident.id.in_(ids))
        )
        result = query.scalars().all()
        return result

    async def save_ai_analysis_id(self, incident_id: int, ai_analysis_id: int):
        await self.db.execute(
            update(ORMIncident)
            .where(ORMIncident.id == incident_id)
            .values(ai_analysis_id=ai_analysis_id)
        )

    async def save_incidents(
        self,
        *,
        incidents: list[Incident],
    ) -> None:
        orm_incidents: list[ORMIncident] = []

        for incident in incidents:
            incident_payload = incident.model_dump(
                exclude={
                    "id",
                    "entities",
                    "related_signals",
                    "metadata",
                }
            )
            incident_payload["incident_type"] = incident.incident_type.value
            incident_payload["severity"] = incident.severity.value
            incident_payload["status"] = incident.status.value

            orm_incident = ORMIncident(
                **incident_payload,
            )

            orm_incidents.append(orm_incident)
            self.db.add(orm_incident)
            await self.db.flush()

            for entity in incident.entities:
                self.db.add(
                    IncidentEntities(
                        entity_id=entity.id,
                        incident_id=orm_incident.id,
                    )
                )

        await self.db.flush()

        signal_repo = SignalRepository(self.db)

        for i, orm_incident in enumerate(orm_incidents):
            # store ids of incidents.
            incidents[i].id = orm_incident.id

            # store id in signals.
            related_signals = incidents[i].related_signals
            signal_ids = [cast(int, s.id) for s in related_signals]
            await signal_repo.save_incident_id(orm_incident.id, signal_ids)
