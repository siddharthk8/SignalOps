import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.config import settings

# File-based logging configuration for application domains

BASE_DIR = Path(__file__).resolve().parents[2]

# Local directory for file-based logs
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str):
    logger = logging.getLogger(name)

    # Avoid attaching multiple handlers to the same logger
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File logging is disabled in test environments
    if not settings.testing:
        handler = TimedRotatingFileHandler(
            LOG_DIR / f"{name}.log",
            when="midnight",
            interval=1,
            backupCount=20,
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
        logger.propagate = False

    return logger


# Domain-specific logger for authentication & user/account related events
auth_logger = get_logger("auth")
