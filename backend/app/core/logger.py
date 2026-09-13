import logging

from app.core.config import settings


def get_logger(name: str):
    logger = logging.getLogger(name)

    # Avoid attaching multiple handlers to the same logger
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # No logging handlers during tests
    if settings.testing:
        return logger

    # Logs go to stderr/stdout, which Docker captures
    handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)

    # Prevent duplicate logging through the root logger
    logger.propagate = False

    return logger


# Domain-specific logger for authentication & user/account related events
auth_logger = get_logger("auth")
