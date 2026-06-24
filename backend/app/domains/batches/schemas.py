from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BatchBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class Batch(BatchBaseModel):
    id: int
    created_at: datetime


class PaginatedBatchResponse(BatchBaseModel):
    batches: list[Batch]
    total: int
    skip: int
    limit: int
    has_more: bool
