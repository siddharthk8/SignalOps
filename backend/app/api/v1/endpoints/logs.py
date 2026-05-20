from fastapi import APIRouter, status

from app.engine.pipeline.orchestration import log_pipeline
from app.schemas.log import LogBatchRequest, LogBatchResponse

router = APIRouter()


@router.post(
    "/",
    response_model=LogBatchResponse,
    status_code=status.HTTP_200_OK,
    name="ingest_logs",
)
async def ingest_logs(data: LogBatchRequest):
    return await log_pipeline.process(data)
