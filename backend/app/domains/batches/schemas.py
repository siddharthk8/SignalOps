from datetime import datetime

from pydantic import BaseModel, ConfigDict


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class Batch(_BaseModel):
    id: int
    created_at: datetime
