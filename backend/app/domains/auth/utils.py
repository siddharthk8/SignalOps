import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.db.models.user import User
from app.domains.auth.schemas import RefreshToken

ALGORITHM = settings.password_hash_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(UTC)
    token_expiration = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": token_expiration, "iat": now})

    print("CREATING TOKEN")
    # jwt usage
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key.get_secret_value(), algorithm=ALGORITHM
    )
    return encoded_jwt


def get_access_token_data(token: str) -> dict[str, Any] | None:
    try:
        decoded_jwt = jwt.decode(
            token, settings.secret_key.get_secret_value(), algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        return None
    return decoded_jwt


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def get_refresh_token_hash(refresh_token: str) -> str:
    # Do not use Argon2 here since it is intentionally slow (meant for passwords).
    # For refresh tokens, fast hashing (SHA-256) is sufficient.
    return hashlib.sha256(refresh_token.encode()).hexdigest()


def create_refresh_token_obj(user: User, refresh_token: str) -> RefreshToken:
    token_hash = get_refresh_token_hash(refresh_token)
    expiration_time = datetime.now(UTC) + timedelta(
        days=settings.refresh_token_expire_days
    )

    a = RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expiration_time)
    return a
