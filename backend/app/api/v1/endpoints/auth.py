from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.domains.auth.dependencies import get_current_active_user
from app.domains.auth.schemas import TokenResponse, UserCreate, UserPrivate
from app.domains.auth.service import create_token, register_user

router = APIRouter()


@router.post(
    "/register", response_model=UserPrivate, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return await register_user(user, db)


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await create_token(form_data, db)


@router.get("/me")
async def get_current_user(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
):
    return current_user
