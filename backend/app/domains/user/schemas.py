import uuid
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
    model_validator,
)


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Reserved for future public user endpoints, its not yet in use.
# class UserPublic(BaseUserSchema):
#     id: uuid.UUID
#     first_name: str
#     last_name: str
#     profile_image_path: str | None


class UserPrivate(BaseUserSchema):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    profile_image_path: str | None
    is_active: bool


class UserUpdate(BaseUserSchema):
    first_name: str | None = None
    last_name: str | None = None


PasswordField = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=50,
        strip_whitespace=True,
    ),
]


class PasswordValidationMixin(BaseUserSchema):
    @field_validator(
        "password",
        "current_password",
        "new_password",
        check_fields=False,
    )
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(password) > 50:
            raise ValueError("Password must not exceed 50 characters")
        if not any(not ch.isalnum() for ch in password):
            raise ValueError("Password must contain a special character")
        if not any(ch.isalpha() for ch in password):
            raise ValueError("Password must contain a letter")
        if not any(ch.isdigit() for ch in password):
            raise ValueError("Password must contain a digit")
        if any(ch.isspace() for ch in password):
            raise ValueError("Password must not contain blank spaces")
        return password


class UserCreate(PasswordValidationMixin):
    id: uuid.UUID | None = None
    first_name: str
    last_name: str
    email: EmailStr
    password: PasswordField

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.strip().lower()

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


class UserPasswordChange(PasswordValidationMixin):
    current_password: PasswordField
    new_password: PasswordField

    @model_validator(mode="after")
    def validate_password_change(self):
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password.")
        return self
