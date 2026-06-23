from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.domains.auth import service
from app.domains.auth.schemas import (
    RefreshTokenRequest,
    RefreshTokenResponse,
    TokenResponse,
)
from app.domains.users.dependencies import CurrentUser

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await service.create_token(form_data, db)


@router.post(
    "/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK
)
async def refresh_token(
    refresh_token_data: RefreshTokenRequest,
    db: Annotated[Session, Depends(get_db)],
):
    return await service.refresh_token(refresh_token_data, db)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_refresh_token(
    refresh_token_data: RefreshTokenRequest,
    _current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return await service.revoke_refresh_token(refresh_token_data, db)
