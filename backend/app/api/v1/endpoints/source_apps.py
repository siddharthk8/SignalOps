from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.config import settings
from app.core.rate_limiter.dependencies import user_rate_limit
from app.db.core import DBSessionDep
from app.domains.source_app import service
from app.domains.source_app.schemas import (
    PaginatedBatchesResponse,
    PaginatedSourceAppResponse,
    SourceAppAccessTokenGenerationResponse,
    SourceAppAccessTokenRequest,
    SourceAppModel,
    SourceAppRequest,
)
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/access-token",
    response_model=SourceAppAccessTokenGenerationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(user_rate_limit(capacity=4, refill_rate=0.01))],
)
async def generate_source_app_access_token(
    data: SourceAppAccessTokenRequest,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.generate_source_app_access_token(data, current_user, db)


@router.delete(
    "/access-token",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=4, refill_rate=0.01))],
)
async def delete_source_app_access_token(
    data: SourceAppAccessTokenRequest,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.delete_source_app_access_token(data, current_user, db)


@router.get(
    "",
    response_model=PaginatedSourceAppResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=30, refill_rate=0.5))],
)
async def get_source_apps(
    current_user: CurrentUser,
    db: DBSessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = settings.source_apps_per_page,
):
    return await service.get_source_apps(skip, limit, current_user, db)


@router.post(
    "",
    response_model=SourceAppModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(user_rate_limit(capacity=10, refill_rate=0.1))],
)
async def create_source_app(
    data: SourceAppRequest,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.create_source_app(data, current_user, db)


@router.get(
    "/{source_app_id}",
    response_model=SourceAppModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=10, refill_rate=0.1))],
)
async def get_source_app(
    source_app_id: int,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.get_source_app(source_app_id, current_user, db)


@router.delete(
    "/{source_app_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=5, refill_rate=0.05))],
)
async def delete_source_app(
    source_app_id: int,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.delete_source_app(source_app_id, current_user, db)


@router.get(
    "/{source_app_id}/batches",
    response_model=PaginatedBatchesResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=30, refill_rate=0.5))],
)
async def get_source_app_batches(
    current_user: CurrentUser,
    source_app_id: int,
    db: DBSessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = settings.batches_per_page,
):
    return await service.get_source_app_batches(
        skip, limit, source_app_id, current_user, db
    )
