from pydantic import BaseModel, ConfigDict


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class GetOAuthConnection(_BaseModel):
    provider: str


class GetOAuthConnections(_BaseModel):
    connections: list[GetOAuthConnection]


class GoogleLoginRequest(BaseModel):
    credential: str
