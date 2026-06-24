from sqlalchemy.orm import Session

from app.db.repositories.batch import BatchRepository
from app.domains.batches.schemas import Batch, PaginatedBatchResponse
from app.domains.users.dependencies import CurrentUser


async def get_batches(
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
