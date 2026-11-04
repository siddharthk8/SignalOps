from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.incident import Incident as ORMIncident
from app.db.repositories.entity_incident import EntityIncidentRepository
from app.db.repositories.signal_incident import SignalIncidentRepository
from app.enums.incident import IncidentStatus
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

    async def get_by_id(self, id: int) -> ORMIncident | None:
        query = await self.db.execute(select(ORMIncident).where(ORMIncident.id == id))
        result = query.scalar_one_or_none()
        return result

    async def save_resolved_at(self, id: int):
        await self.db.execute(
            update(ORMIncident)
            .where(ORMIncident.id == id)
            .values(resolved_at=datetime.now(UTC), status=IncidentStatus.RESOLVED)
        )

    async def get_daily_incidents_over_last_30_days_by_user(self, user_id: UUID):
        start_date = datetime.now(UTC) - timedelta(days=30)

        query = await self.db.execute(
            select(
                func.date(ORMIncident.detected_at).label("date"),
                func.count(ORMIncident.id).label("count"),
            )
            .where(
                ORMIncident.user_id == user_id, ORMIncident.detected_at >= start_date
            )
            .group_by(func.date(ORMIncident.detected_at))
            .order_by(func.date(ORMIncident.detected_at))
        )
        return query.all()

    async def get_last_5_incidents_by_user(
        self, user_id: UUID
    ) -> Sequence[ORMIncident]:
        query = await self.db.execute(
            select(ORMIncident)
            .where(ORMIncident.user_id == user_id)
            .order_by(ORMIncident.detected_at.desc())
            .limit(5)
        )
        return query.scalars().all()

    async def get_count_unresolved_events_by_user(self, user_id: UUID) -> int:
        query = await self.db.execute(
            select(func.count())
            .select_from(ORMIncident)
            .where(ORMIncident.user_id == user_id, ORMIncident.resolved_at.is_(None))
        )
        count = query.scalar()
        return count or 0

    async def get_count_by_user(self, user_id: UUID) -> int:
        query = await self.db.execute(
            select(func.count())
            .select_from(ORMIncident)
            .where(ORMIncident.user_id == user_id)
        )
        count = query.scalar()
        return count or 0

    async def save(
        self,
        *,
        user_id: UUID,
        batch_id: int,
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
            incident_payload["user_id"] = user_id
            incident_payload["batch_id"] = batch_id

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
