from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.db.repositories.batch_repository import BatchRepository
from app.db.repositories.source_app_respository import SourceAppRepository
from app.engine.pipeline.orchestration import LogPipeline
from app.schemas.analysis import IncidentAnalysis
from app.schemas.log import LogBatchRequest

router = APIRouter()


@router.post(
    "/",
    response_model=list[IncidentAnalysis],
    status_code=status.HTTP_200_OK,
    name="ingest_logs",
)
async def ingest_logs(data: LogBatchRequest, db: Annotated[Session, Depends(get_db)]):
    # get source app
    source_app_orm = SourceAppRepository(db).get_by_id(data.source_app_id)
    if source_app_orm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source app not found."
        )

    # create batch
    batch_orm = BatchRepository(db).create_and_get_batch(source_app_orm.id)

    pipeline = LogPipeline(db, batch_orm, source_app_orm)
    return await pipeline.process(data.logs)
