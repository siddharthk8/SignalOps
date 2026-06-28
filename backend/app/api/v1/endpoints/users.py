from fastapi import APIRouter, UploadFile, status

from app.db.core import DBSessionDep
from app.domains.user import service
from app.domains.user.dependencies import CurrentUser
from app.domains.user.schemas import (
    UserCreate,
    UserPasswordChange,
    UserPrivate,
    UserUpdate,
)

router = APIRouter()


@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: DBSessionDep):
    return await service.create_user(user, db)


@router.get("/me", response_model=UserPrivate)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.patch("/me", response_model=UserPrivate)
async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: DBSessionDep
):
    return await service.update_current_user(data, current_user, db)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user: CurrentUser, db: DBSessionDep):
    return await service.delete_current_user(current_user, db)


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    data: UserPasswordChange,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.change_password(data, current_user, db)


@router.post(
    "/me/profile-image", response_model=UserPrivate, status_code=status.HTTP_200_OK
)
async def upload_profile_image(
    file: UploadFile,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.upload_profile_image(file, current_user, db)


@router.delete("/me/profile-image", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_image(
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.delete_profile_image(current_user, db)
