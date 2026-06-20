from app.engine.parsing.parsers.auth.patterns import AUTH_EVENT_PATTERNS
from app.engine.parsing.parsers.shared.generic_severity import get_generic_severity
from app.enums.common import Severity
from app.enums.event import AuthEventType, GenericEventType
from app.schemas.event import SemanticEvent
from app.schemas.log import PersistedLog

from ...base import BaseParser


class AuthParser(BaseParser):
    @staticmethod
    def get_severity(event_type: AuthEventType | GenericEventType) -> Severity:

        if isinstance(event_type, GenericEventType):
            return get_generic_severity(event_type=event_type)

        if event_type in {
            AuthEventType.ACCOUNT_TAKEOVER_SUSPECTED,
            AuthEventType.SESSION_HIJACK_SUSPECTED,
            AuthEventType.MFA_BYPASS_ATTEMPT,
        }:
            return Severity.CRITICAL

        if event_type in {
            AuthEventType.LOGIN_FAILED,
            AuthEventType.INVALID_CREDENTIALS,
            AuthEventType.ACCOUNT_LOCKED,
            AuthEventType.ACCOUNT_DISABLED,
            AuthEventType.ACCOUNT_SUSPENDED,
            AuthEventType.MFA_FAILED,
            AuthEventType.TOKEN_INVALID,
            AuthEventType.TOKEN_REVOKED,
            AuthEventType.SESSION_INVALID,
            AuthEventType.PASSWORD_CHANGE_FAILED,
            AuthEventType.PASSWORD_RESET_FAILED,
            AuthEventType.SUSPICIOUS_LOGIN,
            AuthEventType.IMPOSSIBLE_TRAVEL_DETECTED,
            AuthEventType.USER_DELETED,
            AuthEventType.AUTH_PROVIDER_UNAVAILABLE,
            AuthEventType.OAUTH_ERROR,
            AuthEventType.SSO_FAILURE,
            AuthEventType.LDAP_AUTH_FAILURE,
        }:
            return Severity.HIGH

        if event_type in {
            AuthEventType.USER_NOT_FOUND,
            AuthEventType.SESSION_EXPIRED,
            AuthEventType.SESSION_TERMINATED,
            AuthEventType.TOKEN_EXPIRED,
            AuthEventType.TOKEN_REFRESH_FAILED,
            AuthEventType.MFA_REQUIRED,
            AuthEventType.MFA_CHALLENGE_SENT,
            AuthEventType.PASSWORD_RESET_REQUESTED,
            AuthEventType.PASSWORD_POLICY_VIOLATION,
            AuthEventType.EMAIL_VERIFICATION_SENT,
            AuthEventType.AUTH_SERVICE_ERROR,
        }:
            return Severity.MEDIUM

        return Severity.LOW

    def parse(self, log: PersistedLog, sequence: int) -> SemanticEvent | None:
        return self.global_parser(
            log=log,
            sequence=sequence,
            PATTERNS=AUTH_EVENT_PATTERNS,
        )
