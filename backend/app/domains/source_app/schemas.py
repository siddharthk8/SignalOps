from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domains.batches.schemas import Batch


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class SourceAppModel(_BaseModel):
    id: int
    name: str
    app_type: str
    created_at: datetime


class PaginatedSourceAppResponse(_BaseModel):
    batches: list[SourceAppModel]
    total: int
    skip: int
    limit: int
    has_more: bool


class PaginatedBatchResponse(_BaseModel):
    batches: list[Batch]
    total: int
    skip: int
    limit: int
    has_more: bool
