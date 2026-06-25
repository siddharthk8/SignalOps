import uuid

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.domains.users.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: uuid.UUID) -> User | None:
        return self.db.get(User, id)

    def get_by_email(self, email: EmailStr) -> User | None:
        return self.db.execute(
            select(User).where(User.email == email.lower())
        ).scalar_one_or_none()

    def check_exists_by_email(self, email: str) -> bool:
        return (
            self.db.execute(
                select(User.id).where(User.email == email)
            ).scalar_one_or_none()
            is not None
        )

    def check_exists_by_id(self, id: uuid.UUID) -> bool:
        return (
            self.db.execute(select(User.id).where(User.id == id)).scalar_one_or_none()
            is not None
        )

    def create_user(self, user: UserCreate, password_hash: str):
        db_user = User(**user.model_dump(exclude={"id", "password"}))
        db_user.password_hash = password_hash
        self.db.add(db_user)
        self.db.flush()
        user.id = db_user.id

    def delete_user(self, user: User):
        self.db.delete(user)

    def increment_token_version(self, user: User):
        # Incrementing token_version atomically in the database to avoid race conditions.
        self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(token_version=User.token_version + 1)
        )
