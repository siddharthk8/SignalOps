from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.domains.auth.schemas import TokenResponse
from app.domains.auth.utils import (
    create_access_token,
    get_user,
    verify_password,
)


async def create_token(form_data: OAuth2PasswordRequestForm, db: Session):
    id = form_data.username
    user = get_user(db, UUID(id))

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")
