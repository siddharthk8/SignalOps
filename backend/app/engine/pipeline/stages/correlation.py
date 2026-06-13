from sqlalchemy.orm import Session

from app.engine.correlation.correlator import Correlator
from app.enums.common import SourceAppType
from app.schemas.incident import Incident
from app.schemas.signal import Signal


class CorrelationStage:
    def __init__(self, db: Session):
        self.db = db
        self.correlator = Correlator()

    async def run(
        self, signals: list[Signal], source_app: SourceAppType
    ) -> list[Incident]:
        incidents = self.correlator.process(signals=signals, source_app=source_app)
        return incidents
