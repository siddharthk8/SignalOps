from collections.abc import Sequence
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.incident import Incident as ORMIncident
from app.db.repositories.entity_incident import EntityIncidentRepository
from app.db.repositories.signal_incident import SignalIncidentRepository
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

    async def save(
        self,
        *,
        incidents: list[Incident],
    ) -> None:
        incident_models: list[ORMIncident] = []

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

            incident_model = ORMIncident(**incident_payload)
            incident_models.append(incident_model)

            self.db.add(incident_model)

        await self.db.flush()

        entity_incident_repo = EntityIncidentRepository(self.db)
        signal_incident_repo = SignalIncidentRepository(self.db)

        for i, i_model in enumerate(incident_models):
            # store ids of incidents.
            incidents[i].id = i_model.id

            # mapping entities with incidents
            for entity in incidents[i].entities:
                await entity_incident_repo.save(
                    entity_id=cast(int, entity.id),
                    incident_id=i_model.id,
                )

            # mapping signals with incidents
            for signal in incidents[i].related_signals:
                await signal_incident_repo.save(
                    signal_id=cast(int, signal.id),
                    incident_id=i_model.id,
                )

        await self.db.flush()
