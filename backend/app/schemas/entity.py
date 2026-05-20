from pydantic import (
    BaseModel,
)

from app.schemas.log import (
    EmailField,
    IPField,
    RequestIdField,
    SessionIDField,
    UserField,
)


class Entity(BaseModel):
    user: UserField = None
    email: EmailField | None = None
    ip_address: IPField = None
    session_id: SessionIDField = None
    request_id: RequestIdField | None = None
