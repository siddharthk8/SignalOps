from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import auth_logger
from app.db.core import get_db
from app.db.models.source_app import SourceApp
from app.db.models.user import User
from app.db.repositories.source_app import SourceAppRepository
from app.domains.auth.utils import (
    get_access_token_data,
)
from app.domains.source_app.utils import (
    verify_source_app_secret_access_key,
)
from app.domains.user.utils import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_active_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer"
        },  # this header should be returned with 401, as per OpenAPI standards.
    )

    try:
        payload = get_access_token_data(token)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    id = payload.get("sub")
    if id is None:
        auth_logger.warning(
            "Authentication failed: missing subject claim (sub) in token."
        )
        raise credentials_exception

    user = await get_user(db, UUID(id))
    if user is None:
        auth_logger.warning(
            "Authentication failed: user not found. token_sub=%s",
            id,
        )
        raise credentials_exception

    # Token version mismatch means the user's sessions were revoked
    # (e.g. password change, logout-all-devices, account recovery).
    if payload["tv"] != user.token_version:
        auth_logger.warning(
            "Authentication failed: token version mismatch. user_id=%s token_version=%s current_version=%s",
            user.id,
            payload["tv"],
            user.token_version,
        )
        raise credentials_exception

    if user.is_active is False:
        auth_logger.warning(
            "Authentication failed: inactive user. user_id=%s",
            user.id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


@dataclass
class CurrentUserOrSourceApp:
    user: User
    source_app: SourceApp | None = None


async def get_current_user_or_access_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CurrentUserOrSourceApp:
    access_key, secret_access_key = token.split(".", 1)

    if secret_access_key.startswith(settings.source_app_access_token_prefix):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate API credentials.",  # Keep API in text
            headers={"WWW-Authenticate": "Bearer"},
        )

        source_app_repo = SourceAppRepository(db)
        source_app = await source_app_repo.get_by_access_key(access_key)

        if source_app is None or source_app.secret_access_key_hash is None:
            raise credentials_exception

        if not verify_source_app_secret_access_key(
            secret_access_key,
            source_app.secret_access_key_hash,
        ):
            raise credentials_exception

        user = source_app.user

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return CurrentUserOrSourceApp(
            user=user,
            source_app=source_app,
        )

    # Preserve existing JWT validation.
    user = await get_current_active_user(db, token)

    return CurrentUserOrSourceApp(user=user)


CurrentUserOrAccessToken = Annotated[
    CurrentUserOrSourceApp,
    Depends(get_current_user_or_access_token),
]
