import secrets
import string

from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def generate_access_key() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(17))


def generate_secret_access_key() -> str:
    return settings.source_app_access_token_prefix + secrets.token_urlsafe(32)


def verify_source_app_secret_access_key(plain_token: str, hashed_token: str) -> bool:
    return password_hash.verify(plain_token, hashed_token)


def get_source_app_hashed_secret_access_key(plain_token: str) -> str:
    return password_hash.hash(plain_token)
