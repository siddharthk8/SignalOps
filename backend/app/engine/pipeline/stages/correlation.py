from app.engine.correlation.correlator import Correlator
from app.schemas.incident import Incident
from app.schemas.signal import Signal


class CorrelationStage:
    def __init__(self) -> None:
        self.correlator = Correlator()

    async def run(self, signals: list[Signal]) -> list[Incident]:
        incidents = self.correlator.process(signals=signals)
        return incidents
