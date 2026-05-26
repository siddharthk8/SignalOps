import re
from datetime import UTC, datetime
from ipaddress import ip_address

from pydantic import IPvAnyAddress

from app.enums.logs import LogLevel
from app.schemas.entity import SessionIDField
from app.schemas.log import (
    EmailField,
    JSONIncomingLog,
    LogField,
    RequestIdField,
    TextLogField,
    TokenIDField,
    UserField,
)
from app.shared.constants import (
    ENTITY_USER_ALIASES,
    INCOMING_LOG_SESSION_ALIASES,
    INCOMING_LOG_TOKEN_ALIASES,
)


def normalize_log_for_tokens(message: str) -> str:
    # remove uppercase logs from message(like: "ERROR Database connection timeout" -> "Database connection timeout")
    # this is important for getting precise match_score.
    # As if using above example, "ERROR Database connection timeout" was giving 1.0 for both db_error and db_connection_timeout
    # but removing "ERROR" from it will give us accurate "db_connection_timeout"
    pattern = r"\b(?:{})\b".format(
        "|".join(re.escape(level.value.upper()) for level in LogLevel)
    )
    message = re.sub(pattern, "", message)

    # Remove all key=value patterns from the string (this might cause us to loose important data in few types of logs.Ex: "2026-05-26T10:00:00Z user=u123 event=ORDER_VALIDATION_FAILED order_id=o1001")
    # message = re.sub(r"\b\w+=\S+", "", message)

    # make it lowercase
    message = message.lower()

    # It replaces every punctuation/special character with a space.
    message = re.sub(r"[^a-zA-Z0-9 ]+", " ", message)

    # replace multiple spaces with single space
    message = re.sub(r"\s+", " ", message)

    # replace start & end spaces
    message = message.strip()

    return message


def normalize_log(message: str) -> str:
    # make it lowercase (can't do this in here because, for example if ".. user='Sid' ..", our extraction will store ".. user='sid' ..")
    # message = message.lower()

    # replace punctuation(s) with single space
    # we are not removing every punctuation because we need them to extract: email, ip, timestamp etc...
    message = re.sub(r"""[!,$^{}()[\];"|]+""", " ", message)

    # replace multiple spaces with single space
    message = re.sub(r"\s+", " ", message)

    # replace start & end spaces
    message = message.strip()

    return message


def get_user(log: LogField) -> UserField | None:
    if isinstance(log, JSONIncomingLog):
        if log.user:
            return log.user
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    for m in ENTITY_USER_ALIASES:
        match = re.search(rf"{m}=([\w.@-_]+)", message)
        if match:
            user = match.group(1)
            return user

    return None


def get_email(log: LogField) -> EmailField | None:
    if isinstance(log, JSONIncomingLog):
        if log.email:
            return log.email
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    match = re.search(
        r"email=([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", message
    )
    if match:
        return match.group(1)

    match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", message)
    if match:
        return match.group(1)

    return None


def get_message(log: LogField) -> TextLogField:
    if isinstance(log, JSONIncomingLog):
        if log.message:
            return log.message
    else:
        message = log

    return message


def get_timestamp(log: LogField) -> datetime | None:
    if isinstance(log, JSONIncomingLog):
        if log.timestamp:
            return log.timestamp
    else:
        message = log

    datetime_patterns = [
        # 2026-05-17T14:32:45.123456Z
        (
            r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,6}Z\b",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            True,  # has Z timezone
        ),
        # 2026-05-17T14:32:45.123456
        (
            r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,6}\b",
            "%Y-%m-%dT%H:%M:%S.%f",
            False,
        ),
        # 2026-05-17T14:32:45Z
        (
            r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\b",
            "%Y-%m-%dT%H:%M:%SZ",
            True,
        ),
        # 2026-05-17T14:32:45
        (
            r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b",
            "%Y-%m-%dT%H:%M:%S",
            False,
        ),
        # 2026-05-17 14:32:45.123456
        (
            r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{1,6}\b",
            "%Y-%m-%d %H:%M:%S.%f",
            False,
        ),
        # 2026-05-17 14:32:45
        (
            r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b",
            "%Y-%m-%d %H:%M:%S",
            False,
        ),
    ]

    for pattern, dt_format, has_z in datetime_patterns:
        match = re.search(pattern, message)
        if not match:
            continue

        dt_string = match.group(0)

        try:
            dt = datetime.strptime(dt_string, dt_format)

            # Normalize Z to UTC
            if has_z:
                dt = dt.replace(tzinfo=UTC)

            return dt

        except ValueError:
            continue

    return None


def get_token_id(log: LogField) -> TokenIDField | None:
    if isinstance(log, JSONIncomingLog):
        if log.token_id:
            return log.token_id
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    for m in INCOMING_LOG_TOKEN_ALIASES:
        match = re.search(rf"{m}=([a-zA-Z0-9_-]+)", message)
        if match:
            user = match.group(1)
            return user

    return None


def get_session_id(log: LogField) -> SessionIDField | None:
    if isinstance(log, JSONIncomingLog):
        if log.session_id:
            return log.session_id
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    for m in INCOMING_LOG_SESSION_ALIASES:
        match = re.search(rf"{m}=([a-zA-Z0-9_-]+)", message)
        if match:
            user = match.group(1)
            return user

    return None


def get_request_id(log: LogField) -> RequestIdField | None:
    if isinstance(log, JSONIncomingLog):
        if log.request_id:
            return log.request_id
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    match = re.search(r"request_id=([a-zA-Z0-9_-]+)", message)
    if match:
        user = match.group(1)
        return user

    return None


def get_ip_address(log: LogField) -> IPvAnyAddress | None:
    if isinstance(log, JSONIncomingLog):
        if log.ip_address:
            return log.ip_address
        else:
            message = log.message
    else:
        message = log

    message = normalize_log(message=message)

    IPv4 = r"(?:\d{1,3}\.){3}\d{1,3}"
    IPv6 = r"(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}"
    pattern = rf"\b(?:{IPv4}|{IPv6})\b"

    all_ips = re.findall(pattern, message)
    for c in all_ips:
        try:
            ip = ip_address(c)
            return ip
        except ValueError:
            continue

    return None
