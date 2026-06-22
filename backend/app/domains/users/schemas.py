import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseUserSchema):
    id: uuid.UUID
    first_name: str
    last_name: str


class UserPrivate(BaseUserSchema):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool


class UserUpdate(BaseUserSchema):
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(BaseUserSchema):
    id: uuid.UUID | None = None
    first_name: str
    last_name: str
    email: EmailStr
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=50,
            strip_whitespace=True,
        ),
    ]

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(ch.isupper() for ch in password):
            raise ValueError("Password must contain an uppercase letter")
        if not any(ch.isdigit() for ch in password):
            raise ValueError("Password must contain a digit")
        if any(ch.isspace() for ch in password):
            raise ValueError("Password must not contain any blank space")
        return password

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "sid",
                "last_name": "k",
                "email": "sid@example.com",
                "password": "String123",
            }
        }
    )
