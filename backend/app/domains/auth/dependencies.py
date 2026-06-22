from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.db.models.user import User
from app.domains.auth.utils import (
    get_access_token_data,
    get_user,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_active_user(
    db: Annotated[Session, Depends(get_db)],
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
        raise credentials_exception

    user = get_user(db, UUID(id))
    if user is None:
        raise credentials_exception

    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]
