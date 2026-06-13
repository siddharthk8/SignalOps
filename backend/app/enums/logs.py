from enum import StrEnum


class LogLevel(StrEnum):
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    # Compatibility aliases
    WARN = "warn"
    FATAL = "critical"
