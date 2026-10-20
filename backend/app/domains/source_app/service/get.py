from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.batch import BatchRepository
from app.db.repositories.source_app import SourceAppRepository
from app.domains.batch.schemas import Batch
from app.domains.source_app.schemas import (
    PaginatedBatchesResponse,
    PaginatedSourceAppResponse,
    SourceAppModel,
)
from app.domains.user.dependencies import CurrentUser


async def get_source_app_batches(
    skip: int,
    limit: int,
    source_app_id: int,
    current_user: CurrentUser,
    db: AsyncSession,
):
    batch_repo = BatchRepository(db)
    total_batches = await batch_repo.get_total_batches(source_app_id)

    paginated_batches_orm = await batch_repo.get_paginated_batches(
        source_app_id, skip, limit
    )
    paginated_batches = []

    for b, log_count in paginated_batches_orm:
        b.log_count = log_count
        batch = Batch.model_validate(b)
        paginated_batches.append(batch)

    has_more = False
    if len(paginated_batches) + skip < total_batches:
        has_more = True

    return PaginatedBatchesResponse(
        batches=paginated_batches,
        total=total_batches,
        limit=limit,
        skip=skip,
        has_more=has_more,
    )


async def get_source_apps(
    skip: int, limit: int, current_user: CurrentUser, db: AsyncSession
):
    source_app_repo = SourceAppRepository(db)
    total_source_apps = await source_app_repo.get_total_source_apps(current_user.id)

    paginated_source_apps_orm = await source_app_repo.get_paginated_source_apps(
        current_user.id, skip, limit
    )
    paginated_source_apps = [
        SourceAppModel.model_validate(b) for b in paginated_source_apps_orm
    ]

    has_more = False
    if len(paginated_source_apps) + skip < total_source_apps:
        has_more = True

    return PaginatedSourceAppResponse(
        source_apps=paginated_source_apps,
        total=total_source_apps,
        limit=limit,
        skip=skip,
        has_more=has_more,
    )


async def get_source_app(
    source_app_id: int, current_user: CurrentUser, db: AsyncSession
):
    source_app_repo = SourceAppRepository(db)
    source_app = await source_app_repo.get_by_id(source_app_id)

    if source_app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source app does not exists."
        )

    if source_app.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this source app.",
        )

    return SourceAppModel.model_validate(source_app)
