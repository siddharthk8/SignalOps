from fastapi import APIRouter, Depends, HTTPException, status

from app.core.rate_limiter.dependencies import (
    access_token_user_rate_limit,
)
from app.db.core import DBSessionDep
from app.db.repositories.batch import BatchRepository
from app.db.repositories.source_app import SourceAppRepository
from app.domains.user.dependencies import CurrentUserOrAccessToken
from app.engine.pipeline.orchestration import LogPipeline
from app.schemas.analysis import IncidentAnalysis
from app.schemas.log import LogBatchRequest

router = APIRouter()


@router.post(
    "",
    response_model=list[IncidentAnalysis],
    status_code=status.HTTP_200_OK,
    name="ingest_logs",
    dependencies=[Depends(access_token_user_rate_limit(capacity=20, refill_rate=0.05))],
)
async def ingest_logs(
    data: LogBatchRequest,
    current: CurrentUserOrAccessToken,
    db: DBSessionDep,
):
    source_app_orm = current.source_app
    current_user = current.user

    if source_app_orm is not None:
        # check source app (Access Token request)
        if data.source_app_id != source_app_orm.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Source app does not match access token.",
            )
    else:
        # get source app (JWT request)
        source_app_orm = await SourceAppRepository(db).get_by_id(data.source_app_id)
        if source_app_orm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Source app not found."
            )

    if source_app_orm.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action.",
        )

    # create batch
    batch_orm = await BatchRepository(db).save_and_get_batch(source_app_orm.id)

    pipeline = LogPipeline(db, current_user, batch_orm, source_app_orm)
    return await pipeline.process(data.logs)
