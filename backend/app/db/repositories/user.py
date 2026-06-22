import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.domains.users.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: uuid.UUID) -> User | None:
        return self.db.get(User, id)

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
