from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import auth_logger
from app.db.core import get_db
from app.db.models.user import User
from app.domains.auth.utils import (
    get_access_token_data,
)
from app.domains.user.utils import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_active_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },  # this header should be returned with 401, as per OpenAPI standards.
    )

    payload = get_access_token_data(token)
    if payload is None:
        raise credentials_exception

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
