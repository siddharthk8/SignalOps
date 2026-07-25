from fastapi import APIRouter, Depends, status

from app.core.rate_limiter.dependencies import user_rate_limit
from app.db.core import DBSessionDep
from app.domains.batch import service
from app.domains.batch.schemas import GetBatch
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.get(
    "/{batch_id}",
    response_model=GetBatch,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=30, refill_rate=0.5))],
)
async def get_batch(batch_id: int, current_user: CurrentUser, db: DBSessionDep):
    return await service.get_batch(batch_id, current_user, db)
