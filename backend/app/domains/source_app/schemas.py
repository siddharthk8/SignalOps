from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domains.batch.schemas import Batch
from app.enums.common import SourceAppType


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class SourceAppModel(_BaseModel):
    id: int
    name: str
    app_type: str
    created_at: datetime


class SourceAppRequest(_BaseModel):
    name: str
    app_type: SourceAppType


class PaginatedSourceAppResponse(_BaseModel):
    source_apps: list[SourceAppModel]
    total: int
    skip: int
    limit: int
    has_more: bool


class PaginatedBatchesResponse(_BaseModel):
    batches: list[Batch]
    total: int
    skip: int
    limit: int
    has_more: bool
