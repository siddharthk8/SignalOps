from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.core import get_db
from app.domains.source_app import service
from app.domains.source_app.schemas import (
    PaginatedBatchResponse,
    PaginatedSourceAppResponse,
)
from app.domains.users.dependencies import CurrentUser

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedSourceAppResponse,
    status_code=status.HTTP_200_OK,
)
async def get_source_apps(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = settings.source_apps_per_page,
):
    return await service.get_source_apps(skip, limit, current_user, db)


@router.get(
    "/{source_app_id}/batches",
    response_model=PaginatedBatchResponse,
    status_code=status.HTTP_200_OK,
)
async def get_source_app_batches(
    current_user: CurrentUser,
    source_app_id: int,
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = settings.batches_per_page,
):
    return await service.get_source_app_batches(
        skip, limit, source_app_id, current_user, db
    )
