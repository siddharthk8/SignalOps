from collections import defaultdict
from datetime import UTC, datetime

from app.engine.rules.base import BaseRule
from app.engine.rules.utility import events_in_last_minutes, threshold_window
from app.enums.common import Severity
from app.enums.event import AuthEventType, GenericEventType
from app.enums.rule import GenericSignalType
from app.schemas.event import SemanticEvent
from app.schemas.signal import Signal


class GenericRule(BaseRule):
    BRUTE_FORCE_THRESHOLD = 8
    ERROR_RATE_THRESHOLD = 15
    SERVICE_FAILURE_THRESHOLD = 5
    DEGRADATION_THRESHOLD = 10

    def evaluate(self, events: list[SemanticEvent]) -> list[Signal]:

        return [
            *self._detect_brute_force_attempt(events),
            *self._detect_high_error_rate(events),
            *self._detect_cascading_service_failure(events),
            *self._detect_downstream_service_degradation(events),
        ]

    # BRUTE FORCE ATTEMPT (AUTH DOMAIN)
    def _detect_brute_force_attempt(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:

        window = threshold_window(
            events=events,
            minutes=2,
            threshold=self.BRUTE_FORCE_THRESHOLD,
            functional_check=lambda e: (
                e.event_type
                in {
                    AuthEventType.LOGIN_FAILED,
                    AuthEventType.INVALID_CREDENTIALS,
                    AuthEventType.MFA_FAILED,
                    AuthEventType.TOKEN_INVALID,
                    AuthEventType.ACCOUNT_LOCKED,
                    AuthEventType.SUSPICIOUS_LOGIN,
                }
            ),
        )

        if len(window) < self.BRUTE_FORCE_THRESHOLD:
            return []

        return [
            Signal(
                signal_type=GenericSignalType.BRUTE_FORCE_ATTEMPT,
                severity=Severity.HIGH,
                confidence=0.95,
                source_app=window[0].source_app,
                entity=window[0].entity,
                supporting_events=[e.sequence for e in window],
                metadata={
                    "attempt_count": len(window),
                    "window_minutes": 2,
                },
                triggered_at=datetime.now(UTC),
            )
        ]

    def _detect_high_error_rate(self, events: list[SemanticEvent]) -> list[Signal]:
        recent = events_in_last_minutes(events, minutes=5)

        errors = [
            e
            for e in recent
            if e.event_type
            in {
                GenericEventType.INTERNAL_SERVICE_ERROR,
                GenericEventType.SERVICE_UNAVAILABLE,
                GenericEventType.REQUEST_TIMEOUT,
                GenericEventType.NETWORK_ERROR,
                GenericEventType.DEPENDENCY_FAILURE,
            }
        ]

        if len(errors) < self.ERROR_RATE_THRESHOLD:
            return []

        return [
            Signal(
                signal_type=GenericSignalType.HIGH_ERROR_RATE_PATTERN,
                severity=Severity.MEDIUM,
                confidence=0.90,
                source_app=errors[0].source_app,
                entity=errors[0].entity,
                supporting_events=[e.sequence for e in errors],
                metadata={"error_count": len(errors)},
                triggered_at=datetime.now(UTC),
            )
        ]

    def _detect_cascading_service_failure(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        """
        A cascading service failure is a domino-effect phenomenon in interconnected systems
        where the failure or degradation of one component overloads the remaining healthy components,
        causing them to collapse sequentially.
        """
        signals: list[Signal] = []

        failures_by_source: dict[str, list[SemanticEvent]] = defaultdict(list)

        for e in events:
            if e.event_type not in {
                GenericEventType.SERVICE_UNAVAILABLE,
                GenericEventType.INTERNAL_SERVICE_ERROR,
                GenericEventType.DEPENDENCY_FAILURE,
                GenericEventType.DOWNSTREAM_SERVICE_FAILURE,
            }:
                continue

            failures_by_source[e.source_app].append(e)

        for service_events in failures_by_source.values():
            window_events = threshold_window(
                events=service_events,
                minutes=3,
                threshold=self.SERVICE_FAILURE_THRESHOLD,
            )

            if len(window_events) < self.SERVICE_FAILURE_THRESHOLD:
                continue

            signals.append(
                Signal(
                    signal_type=GenericSignalType.CASCADING_SERVICE_FAILURE,
                    severity=Severity.HIGH,
                    confidence=0.92,
                    source_app=window_events[0].source_app,
                    entity=window_events[0].entity,
                    supporting_events=[e.sequence for e in window_events],
                    metadata={"failure_count": len(window_events)},
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_downstream_service_degradation(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        """
        Downstream service degradation means a system or component that your application depends on
        (such as a database, third-party API, or microservice) is functioning poorly.
        It is not completely broken (which would be an outage),
        but it is slow or returning intermittent errors, causing your own service to struggle.
        """

        degradation = [
            e
            for e in events
            if e.event_type
            in {
                GenericEventType.SERVICE_TIMEOUT,
                GenericEventType.REQUEST_TIMEOUT,
                GenericEventType.NETWORK_ERROR,
                GenericEventType.CONNECTION_TIMEOUT,
            }
        ]

        if len(degradation) < self.DEGRADATION_THRESHOLD:
            return []

        return [
            Signal(
                signal_type=GenericSignalType.DOWNSTREAM_SERVICE_DEGRADATION,
                severity=Severity.MEDIUM,
                confidence=0.88,
                source_app=degradation[0].source_app,
                entity=degradation[0].entity,
                supporting_events=[e.sequence for e in degradation],
                metadata={"degradation_count": len(degradation)},
                triggered_at=datetime.now(UTC),
            )
        ]
