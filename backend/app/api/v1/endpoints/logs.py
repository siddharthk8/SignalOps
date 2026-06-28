from fastapi import APIRouter, HTTPException, status

from app.db.core import DBSessionDep
from app.db.repositories.batch import BatchRepository
from app.db.repositories.source_app import SourceAppRepository
from app.domains.user.dependencies import CurrentUser
from app.engine.pipeline.orchestration import LogPipeline
from app.schemas.analysis import IncidentAnalysis
from app.schemas.log import LogBatchRequest

router = APIRouter()


@router.post(
    "",
    response_model=list[IncidentAnalysis],
    status_code=status.HTTP_200_OK,
    name="ingest_logs",
)
async def ingest_logs(
    data: LogBatchRequest,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    # get source app
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

    pipeline = LogPipeline(db, batch_orm, source_app_orm)
    return await pipeline.process(data.logs)
