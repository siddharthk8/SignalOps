import uuid

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.domains.user.schemas import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: uuid.UUID) -> User | None:
        return await self.db.get(User, id)

    async def get_by_email(self, email: EmailStr) -> User | None:
        query = await self.db.execute(select(User).where(User.email == email.lower()))
        result = query.scalar_one_or_none()
        return result

    async def check_exists_by_email(self, email: str) -> bool:
        query = await self.db.execute(select(User.id).where(User.email == email))
        result = query.scalar_one_or_none()
        return result is not None

    async def check_exists_by_id(self, id: uuid.UUID) -> bool:
        query = await self.db.execute(select(User.id).where(User.id == id))
        result = query.scalar_one_or_none()
        return result is not None

    async def save_user(self, user: UserCreate, password_hash: str):
        db_user = User(**user.model_dump(exclude={"id", "password", "otp"}))
        db_user.password_hash = password_hash
        self.db.add(db_user)
        await self.db.flush()
        user.id = db_user.id

    async def remove_user(self, user: User):
        await self.db.delete(user)

    async def increment_token_version(self, user: User):
        # Incrementing token_version atomically in the database to avoid race conditions.
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(token_version=User.token_version + 1)
        )
