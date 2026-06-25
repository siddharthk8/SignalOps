import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import boto3
import jwt
from fastapi.templating import Jinja2Templates
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


# refresh token utils
def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def get_refresh_token_hash(refresh_token: str) -> str:
    # Do not use Argon2 here since it is intentionally slow (meant for passwords).
    # For refresh tokens, fast hashing (SHA-256) is sufficient.
    # Also passwords are easier to guess, but not refresh_tokens.
    return hashlib.sha256(refresh_token.encode()).hexdigest()


def create_refresh_token_obj(user: User, refresh_token: str) -> RefreshToken:
    token_hash = get_refresh_token_hash(refresh_token)
    expiration_time = datetime.now(UTC) + timedelta(
        days=settings.refresh_token_expire_days
    )

    a = RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expiration_time)
    return a


# email utils
templates = Jinja2Templates(directory="templates")


def _get_boto3_ses_client():
    return boto3.client(
        "ses",
        region_name=settings.ses_region,
        aws_access_key_id=(
            settings.aws_access_key_id.get_secret_value()
            if settings.aws_access_key_id
            else None
        ),
        aws_secret_access_key=(
            settings.aws_secret_access_key.get_secret_value()
            if settings.aws_secret_access_key
            else None
        ),
    )


async def send_reset_password_email(*, to_email: str, first_name: str, token: str):
    reset_link = f"{settings.frontend_url}/reset-password?token={token}"

    text_body = f"""Hi {first_name},

We received a request to reset your password for your SignalOps account.

You can set a new password by clicking the link below:
{reset_link}

For your security, this link will expire in {settings.reset_token_expire_minutes} minutes.

If you did not request a password reset, you can safely ignore this email. Your password will remain unchanged.

Best regards,  
The SignalOps Team
"""

    html_template = templates.env.get_template("email/password_reset.html")
    html_body = html_template.render(
        first_name=first_name,
        reset_link=reset_link,
        minutes=settings.reset_token_expire_minutes,
    )

    ses_client = _get_boto3_ses_client()
    ses_client.send_email(
        Source=settings.mail_from,
        Destination={
            "ToAddresses": [to_email],
        },
        Message={
            "Subject": {"Data": "Reset Your Password - SignalOps", "Charset": "UTF-8"},
            "Body": {
                "Text": {"Data": text_body, "Charset": "UTF-8"},
                "Html": {"Data": html_body, "Charset": "UTF-8"},
            },
        },
    )


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def get_reset_token_hash(reset_token: str) -> str:
    return hashlib.sha256(reset_token.encode()).hexdigest()
