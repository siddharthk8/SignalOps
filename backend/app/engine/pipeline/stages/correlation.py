from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.incident import IncidentRepository
from app.engine.correlation.correlator import Correlator
from app.enums.common import SourceAppType
from app.schemas.incident import Incident
from app.schemas.signal import Signal


class CorrelationStage:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.correlator = Correlator()
        self.incident_repo = IncidentRepository(db)

    async def run(
        self, signals: list[Signal], source_app: SourceAppType
    ) -> list[Incident]:
        incidents = self.correlator.process(signals=signals, source_app=source_app)

        # save incidents in db
        await self.incident_repo.save(incidents=incidents)

        return incidents
