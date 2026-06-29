from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.incident import IncidentRepository
from app.engine.correlation.correlator import Correlator
from app.enums.common import SourceAppType
from app.schemas.incident import Incident
from app.schemas.signal import Signal


class CorrelationStage:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user
        self.correlator = Correlator()
        self.incident_repo = IncidentRepository(db)

    async def run(
        self, signals: list[Signal], source_app: SourceAppType
    ) -> list[Incident]:
        incidents = self.correlator.process(signals=signals, source_app=source_app)

        # save incidents in db
        await self.incident_repo.save(user_id=self.current_user.id, incidents=incidents)

        return incidents
