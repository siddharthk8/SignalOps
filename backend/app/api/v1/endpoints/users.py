from fastapi import APIRouter, Depends, UploadFile, status

from app.core.rate_limiter.dependencies import public_rate_limit, user_rate_limit
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


@router.post(
    "",
    response_model=UserPrivate,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(public_rate_limit(capacity=5, refill_rate=0.01))],
)
async def create_user(user: UserCreate, db: DBSessionDep):
    return await service.create_user(user, db)


@router.get(
    "/me",
    response_model=UserPrivate,
    dependencies=[Depends(user_rate_limit(capacity=60, refill_rate=1))],
)
async def get_current_user(current_user: CurrentUser):
    return current_user


@router.patch(
    "/me",
    response_model=UserPrivate,
    dependencies=[Depends(user_rate_limit(capacity=10, refill_rate=0.1))],
)
async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: DBSessionDep
):
    return await service.update_current_user(data, current_user, db)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=2, refill_rate=0.005))],
)
async def delete_current_user(current_user: CurrentUser, db: DBSessionDep):
    return await service.delete_current_user(current_user, db)


@router.post(
    "/me/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=3, refill_rate=0.01))],
)
async def change_password(
    data: UserPasswordChange,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.change_password(data, current_user, db)


@router.post(
    "/me/profile-image",
    response_model=UserPrivate,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=2, refill_rate=0.05))],
)
async def upload_profile_image(
    file: UploadFile,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.upload_profile_image(file, current_user, db)


@router.delete(
    "/me/profile-image",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=5, refill_rate=0.05))],
)
async def delete_profile_image(
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.delete_profile_image(current_user, db)
