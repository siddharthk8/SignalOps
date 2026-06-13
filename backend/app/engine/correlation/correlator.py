from app.engine.correlation.utils import (
    build_incident,
    group_signals,
    match_rules,
)
from app.enums.common import SourceAppType
from app.enums.incident import IncidentType
from app.schemas.incident import Incident
from app.schemas.signal import Signal


class Correlator:
    """
    Core correlation orchestrator.

    Responsibility: Generate incidents
    """

    def process(
        self, signals: list[Signal], source_app: SourceAppType
    ) -> list[Incident]:
        """
        Entry point for correlation pipeline.
        """

        if not signals:
            return []

        # 1. Group signals by entity details/values
        grouped_signals = group_signals(signals, source_app)

        all_incidents: list[Incident] = []

        # 2. Process each group independently
        for signal_group in grouped_signals.values():
            # 3. Apply correlation rules on grouped signals
            matched_incident_types: set[IncidentType] = match_rules(signal_group)

            # 4. Build incidents for each matched rule
            for incident_type in matched_incident_types:
                incident = build_incident(
                    signals=signal_group,
                    incident_type=incident_type,
                )

                all_incidents.append(incident)

        return all_incidents
