from sqlalchemy.orm import Session

from app.db.repositories.batch import BatchRepository
from app.db.repositories.source_app import SourceAppRepository
from app.domains.batches.schemas import Batch
from app.domains.source_app.schemas import (
    PaginatedBatchResponse,
    PaginatedSourceAppResponse,
    SourceAppModel,
)
from app.domains.users.dependencies import CurrentUser


async def get_source_app_batches(
    skip: int, limit: int, source_app_id: int, current_user: CurrentUser, db: Session
):
    batch_repo = BatchRepository(db)
    total_batches = batch_repo.get_total_batches(source_app_id)

    paginated_batches_orm = batch_repo.get_paginated_batches(source_app_id, skip, limit)
    paginated_batches = [Batch.model_validate(b) for b in paginated_batches_orm]

    has_more = False
    if len(paginated_batches) + skip < total_batches:
        has_more = True

    return PaginatedBatchResponse(
        batches=paginated_batches,
        total=total_batches,
        limit=limit,
        skip=skip,
        has_more=has_more,
    )


async def get_source_apps(
    skip: int, limit: int, current_user: CurrentUser, db: Session
):
    source_app_repo = SourceAppRepository(db)
    total_source_apps = source_app_repo.get_total_source_apps(current_user.id)

    paginated_source_apps_orm = source_app_repo.get_paginated_source_apps(
        current_user.id, skip, limit
    )
    paginated_source_apps = [
        SourceAppModel.model_validate(b) for b in paginated_source_apps_orm
    ]

    has_more = False
    if len(paginated_source_apps) + skip < total_source_apps:
        has_more = True

    return PaginatedSourceAppResponse(
        batches=paginated_source_apps,
        total=total_source_apps,
        limit=limit,
        skip=skip,
        has_more=has_more,
    )
