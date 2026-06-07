from pydantic import (
    BaseModel,
)

from app.schemas.log import (
    EmailField,
    IPField,
    RequestIdField,
    SessionIDField,
    TokenIDField,
    UserField,
)


class Entity(BaseModel):
    id: int | None = None  # db id
    user: UserField = None
    email: EmailField | None = None
    ip_address: IPField = None
    session_id: SessionIDField = None
    token_id: TokenIDField = None
    request_id: RequestIdField | None = None
