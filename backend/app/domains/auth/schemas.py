from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints

from app.domains.users.schemas import PasswordField, PasswordValidationMixin


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    user_id: UUID
    token_hash: str
    is_revoked: bool = False
    expires_at: datetime
    revoked_at: datetime | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: Annotated[EmailStr, StringConstraints(max_length=254)]


class ResetPasswordRequest(PasswordValidationMixin):
    token: str
    new_password: PasswordField
