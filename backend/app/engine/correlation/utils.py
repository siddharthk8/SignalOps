from collections import defaultdict
from datetime import UTC, datetime

from app.enums.common import Severity, SourceAppType
from app.enums.incident import IncidentType
from app.enums.signal import (
    AuthSignalType,
    GenericSignalType,
    OrderSignalType,
    PaymentSignalType,
)
from app.schemas.incident import Incident
from app.schemas.signal import Signal


def group_signals(
    signals: list[Signal], source_app: SourceAppType
) -> dict[str, list[Signal]]:
    """
    Multi-dimensional grouping using entity attributes.

    This ensures correlation works across:
    user, email, ip, session, token, request_id
    """

    groups = defaultdict(list)

    for signal in signals:
        e = signal.entity

        key_parts = []

        if e.user:
            key_parts.append(f"user:{e.user}")

        if e.email:
            key_parts.append(f"email:{e.email}")

        if e.ip_address:
            key_parts.append(f"ip:{e.ip_address}")

        if e.session_id:
            key_parts.append(f"session:{e.session_id}")

        if e.token_id:
            key_parts.append(f"token:{e.token_id}")

        if e.request_id:
            key_parts.append(f"request:{e.request_id}")

        # fallback if nothing exists
        if not key_parts:
            key_parts.append(f"source:{source_app.value}")

        key = "|".join(key_parts)

        groups[key].append(signal)

    return groups


def match_rules(signals: list[Signal]) -> set[IncidentType]:
    incidents: set[IncidentType] = set()
    # using set to avoid incident duplication.
    # to do  multiple group wise incident duplication, we should implement another function to dedupliate_incidents before sengin to fontend.

    signal_types = {s.signal_type for s in signals}

    # ACCOUNT SECURITY
    if (
        AuthSignalType.EXCESSIVE_AUTH_FAILURES in signal_types
        and AuthSignalType.TOKEN_ABUSE_PATTERN in signal_types
    ):
        incidents.add(IncidentType.ACCOUNT_SECURITY)

    if AuthSignalType.POSSIBLE_ACCOUNT_COMPROMISE in signal_types:
        incidents.add(IncidentType.ACCOUNT_SECURITY)

    if AuthSignalType.SUSPICIOUS_SESSION_ACTIVITY in signal_types:
        incidents.add(IncidentType.ACCOUNT_SECURITY)

    # PAYMENT
    if (
        PaymentSignalType.PAYMENT_FAILURE_SPIKE in signal_types
        and PaymentSignalType.PAYMENT_RETRY_STORM in signal_types
    ):
        incidents.add(IncidentType.PAYMENT_OUTAGE)

    # ORDER / FRAUD
    if OrderSignalType.SUSPICIOUS_ORDER_ACTIVITY in signal_types:
        incidents.add(IncidentType.POTENTIAL_FRAUD)

    if OrderSignalType.ORDER_CANCELLATION_SPIKE in signal_types:
        incidents.add(IncidentType.POTENTIAL_FRAUD)

    # INFRASTRUCTURE / GENERIC
    if (
        GenericSignalType.HIGH_ERROR_RATE_PATTERN in signal_types
        or GenericSignalType.DOWNSTREAM_SERVICE_DEGRADATION in signal_types
    ):
        incidents.add(IncidentType.SERVICE_DEGRADATION)

    if GenericSignalType.CASCADING_SERVICE_FAILURE in signal_types:
        incidents.add(IncidentType.PLATFORM_INSTABILITY)

    if GenericSignalType.BRUTE_FORCE_ATTEMPT in signal_types:
        incidents.add(IncidentType.ACCOUNT_SECURITY)

    return incidents


def build_incident(signals: list[Signal], incident_type: IncidentType) -> Incident:
    severity = Severity.LOW

    for signal in signals:
        for event in signal.supporting_events:
            if event.severity == Severity.CRITICAL:
                severity = Severity.CRITICAL
                break
            elif event.severity == Severity.HIGH and severity in (
                Severity.LOW,
                Severity.MEDIUM,
            ):
                severity = Severity.HIGH
            elif event.severity == Severity.MEDIUM and severity == Severity.LOW:
                severity = Severity.MEDIUM

        if severity == Severity.CRITICAL:
            break

    confidence = round(sum(s.confidence for s in signals) / len(signals), 2)

    # merge entity (keep full structure)
    entities = [s.entity for s in signals]

    return Incident(
        # incident_id=...,
        incident_type=incident_type,
        severity=severity,
        confidence=confidence,
        title=_generate_title(incident_type),
        summary=_generate_summary(signals, incident_type),
        entities=entities,
        related_signals=signals,
        first_detected_at=min(s.triggered_at for s in signals),
        last_updated_at=datetime.now(UTC),
    )


# DETERMINISTIC SUMMARY (NO AI)
def _generate_summary(signals: list[Signal], incident_type: IncidentType) -> str:

    primary_entity = signals[0].entity
    count = len(signals)

    user = primary_entity.user or "unknown"
    ip = primary_entity.ip_address or "unknown"

    if incident_type == IncidentType.ACCOUNT_SECURITY:
        return f"{count} security-related signals detected for user {user} from IP {ip}"

    if incident_type == IncidentType.PAYMENT_OUTAGE:
        return f"{count} payment-related anomalies detected across payment flow"

    if incident_type == IncidentType.SERVICE_DEGRADATION:
        return f"{count} signals indicate service degradation in system components"

    if incident_type == IncidentType.POTENTIAL_FRAUD:
        return f"{count} fraud-related behavioral signals detected"

    if incident_type == IncidentType.PLATFORM_INSTABILITY:
        return f"{count} cascading failure signals detected across services"

    return f"{incident_type} detected with {count} correlated signals"


def _generate_title(incident_type: IncidentType) -> str:
    return incident_type.replace("_", " ").title()
