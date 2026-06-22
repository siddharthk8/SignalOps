from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

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
    to_encode.update({"exp": token_expiration})

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
