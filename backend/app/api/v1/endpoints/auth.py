from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.rate_limiter.dependencies import public_rate_limit, user_rate_limit
from app.db.core import DBSessionDep
from app.domains.auth import service
from app.domains.auth.schemas import (
    ForgotPasswordRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    ResetPasswordRequest,
    TokenResponse,
)
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(public_rate_limit(capacity=5, refill_rate=0.2))],
)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSessionDep,
):
    return await service.create_token(form_data, db)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(public_rate_limit(capacity=20, refill_rate=0.5))],
)
async def get_new_access_token(
    refresh_token_data: RefreshTokenRequest,
    db: DBSessionDep,
):
    return await service.get_new_access_token(refresh_token_data, db)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=20, refill_rate=0.5))],
)
async def revoke_refresh_token(
    refresh_token_data: RefreshTokenRequest,
    _current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.revoke_refresh_token(refresh_token_data, db)


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=3, refill_rate=0.01))],
)
async def revoke_all_refresh_tokens(
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.revoke_all_refresh_tokens(current_user, db)


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(public_rate_limit(capacity=3, refill_rate=0.005))],
)
async def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: DBSessionDep,
):
    return await service.forgot_password(data, background_tasks, db)


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(public_rate_limit(capacity=5, refill_rate=0.01))],
)
async def reset_password(
    data: ResetPasswordRequest,
    db: DBSessionDep,
):
    return await service.reset_password(data, db)
