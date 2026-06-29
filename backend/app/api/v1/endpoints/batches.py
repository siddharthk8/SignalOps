from fastapi import APIRouter, status

from app.db.core import DBSessionDep
from app.domains.batch import service
from app.domains.batch.schemas import GetBatch
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.get("/{batch_id}", response_model=GetBatch, status_code=status.HTTP_200_OK)
async def get_batch(batch_id: int, current_user: CurrentUser, db: DBSessionDep):
    return await service.get_batch(batch_id, current_user, db)
