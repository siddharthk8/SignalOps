import hashlib
import secrets

# Google


def generate_secret() -> str:
    """Generate a cryptographically secure random secret."""
    return secrets.token_urlsafe(32)


def hash_secret(value: str) -> str:
    """Return the SHA-256 hash of a secret."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def generate_oauth_login_code() -> str:
    """Generate a cryptographically secure, one-time OAuth login code."""
    return secrets.token_urlsafe(32)


def hash_oauth_login_code(code: str) -> str:
    """Hash an OAuth login code before storing it in the database."""
    return hashlib.sha256(code.encode("utf-8")).hexdigest()
