from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.domains.batch.schemas import Batch
from app.enums.common import SourceAppType


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class SourceAppModel(_BaseModel):
    id: int
    name: str
    app_type: str
    created_at: datetime

    access_key: str | None = None
    secret_access_key_hash: Annotated[
        str | None,
        Field(exclude=True),
    ] = None

    @computed_field
    @property
    def has_access_token(self) -> bool:
        return self.secret_access_key_hash is not None


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


# Tokens
class SourceAppAccessTokenRequest(_BaseModel):
    source_app_id: int


class SourceAppAccessTokenGenerationResponse(_BaseModel):
    access_token: str
