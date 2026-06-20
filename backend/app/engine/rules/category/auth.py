from collections import defaultdict
from datetime import UTC, datetime

from app.engine.rules.base import BaseRule
from app.engine.rules.utils import (
    contains_sequence,
    group_by_user,
    group_by_user_and_filter,
    threshold_window,
)
from app.enums.event import AuthEventType
from app.enums.signal import AuthSignalType
from app.schemas.event import SemanticEvent
from app.schemas.signal import Signal


class AuthRule(BaseRule):
    """
    Authentication-related signal generation.

    Semantic Events
        ↓
    Auth Signals
    """

    FAILED_LOGIN_THRESHOLD = 5
    TOKEN_ABUSE_THRESHOLD = 10
    SESSION_IP_THRESHOLD = 3

    def evaluate(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:

        signals: list[Signal] = []
        signals.extend(self._detect_excessive_auth_failures(events))
        signals.extend(self._detect_possible_account_compromise(events))
        signals.extend(self._detect_suspicious_session_activity(events))
        signals.extend(self._detect_token_abuse(events))

        return signals

    def _detect_excessive_auth_failures(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        FAILURE_EVENTS = {
            AuthEventType.INVALID_CREDENTIALS,
            AuthEventType.LOGIN_FAILED,
            AuthEventType.USER_NOT_FOUND,
            AuthEventType.ACCOUNT_LOCKED,
            AuthEventType.ACCOUNT_DISABLED,
            AuthEventType.ACCOUNT_SUSPENDED,
            AuthEventType.TOKEN_INVALID,
            AuthEventType.TOKEN_REFRESH_FAILED,
            AuthEventType.MFA_FAILED,
            AuthEventType.MFA_BYPASS_ATTEMPT,
            AuthEventType.SESSION_INVALID,
            AuthEventType.SSO_FAILURE,
            AuthEventType.LDAP_AUTH_FAILURE,
        }

        # Group failure events by user
        failures_by_user = group_by_user_and_filter(
            events, functional_check=lambda event: event.event_type in FAILURE_EVENTS
        )

        for user_events in failures_by_user.values():
            window_events = threshold_window(
                events=user_events,
                minutes=5,
                threshold=self.FAILED_LOGIN_THRESHOLD,
            )

            if len(window_events) == 0:
                continue

            signals.append(
                Signal(
                    signal_type=AuthSignalType.EXCESSIVE_AUTH_FAILURES,
                    confidence=0.90,
                    entity=window_events[0].entity,
                    supporting_events=window_events,
                    metadata={
                        "failure_count": len(window_events),
                        "window_minutes": self.FAILED_LOGIN_THRESHOLD,
                        "window_start": window_events[0].timestamp,
                        "window_end": window_events[-1].timestamp,
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_possible_account_compromise(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        events_by_user = group_by_user(events)

        compromise_pattern = [
            AuthEventType.LOGIN_SUCCESS,
            AuthEventType.PASSWORD_CHANGE_FAILED,
            AuthEventType.PASSWORD_CHANGE_SUCCESS,
        ]

        for user_events in events_by_user.values():
            if not contains_sequence(
                user_events,
                compromise_pattern,
            ):
                continue

            signals.append(
                Signal(
                    signal_type=AuthSignalType.POSSIBLE_ACCOUNT_COMPROMISE,
                    confidence=0.80,
                    entity=user_events[0].entity,
                    supporting_events=user_events,
                    metadata={
                        "pattern": [str(x) for x in compromise_pattern],
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_suspicious_session_activity(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        session_ips: dict[str, set] = defaultdict(set)
        session_events: dict[str, list] = defaultdict(list)

        for event in events:
            session_id = event.entity.session_id
            if not session_id:
                continue

            session_events[session_id].append(event)

            ip = event.entity.ip_address
            if not ip:
                continue

            session_ips[session_id].add(ip)

        for session_id, ips in session_ips.items():
            if len(ips) < self.SESSION_IP_THRESHOLD:
                continue

            supporting_events = session_events[session_id]

            signals.append(
                Signal(
                    signal_type=AuthSignalType.SUSPICIOUS_SESSION_ACTIVITY,
                    confidence=0.85,
                    entity=supporting_events[0].entity,
                    supporting_events=supporting_events,
                    metadata={
                        "unique_ip_count": len(ips),
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_token_abuse(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        token_usage = defaultdict(list)

        for event in events:
            if event.event_type not in {
                AuthEventType.TOKEN_ISSUED,
                AuthEventType.TOKEN_REFRESH_SUCCESS,
            }:
                continue

            token_id = event.entity.token_id
            if not token_id:
                continue

            token_usage[token_id].append(event)

        for token_events in token_usage.values():
            if len(token_events) < self.TOKEN_ABUSE_THRESHOLD:
                continue

            signals.append(
                Signal(
                    signal_type=AuthSignalType.TOKEN_ABUSE_PATTERN,
                    confidence=0.90,
                    entity=token_events[0].entity,
                    supporting_events=token_events,
                    metadata={
                        "usage_count": len(token_events),
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals
