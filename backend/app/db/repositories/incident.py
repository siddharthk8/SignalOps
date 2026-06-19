from sqlalchemy.orm import Session

from app.db.models.incident import Incident as ORMIncident
from app.db.models.incident_entities import IncidentEntities
from app.schemas.incident import Incident


class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_incidents(
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
            self.db.add(orm_incident)
            self.db.flush()

            for entity in incident.entities:
                self.db.add(
                    IncidentEntities(
                        entity_id=entity.id,
                        incident_id=orm_incident.id,
                    )
                )

        self.db.flush()

        # store ids of incidents.
        for i, orm_incident in enumerate(orm_incidents):
            incidents[i].id = orm_incident.id
