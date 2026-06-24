from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.domains.batches import service
from app.domains.batches.schemas import PaginatedBatchResponse
from app.domains.users.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/{source_app_id}",
    response_model=PaginatedBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
async def get_batches(
    current_user: CurrentUser,
    source_app_id: int,
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return await service.get_batches(skip, limit, source_app_id, current_user, db)
