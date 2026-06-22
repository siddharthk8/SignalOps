from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.domains.auth import service
from app.domains.auth.dependencies import CurrentUser
from app.domains.auth.schemas import TokenResponse, UserCreate, UserPrivate, UserUpdate

router = APIRouter()


@router.post("/users", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return await service.create_user(user, db)


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await service.create_token(form_data, db)


@router.get("/users/me", response_model=UserPrivate)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.patch("/users/me", response_model=UserPrivate)
async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: Annotated[Session, Depends(get_db)]
):
    return await service.update_current_user(data, current_user, db)
