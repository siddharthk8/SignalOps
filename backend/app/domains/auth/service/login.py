from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.refresh_token import RefreshTokenRepository
from app.domains.auth.schemas import TokenResponse
from app.domains.auth.utils import (
    create_access_token,
    create_refresh_token_obj,
    generate_refresh_token,
    verify_password,
)
from app.domains.users.utils import get_user


async def create_token(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    id = form_data.username
    user = await get_user(db, UUID(id))

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id), "tv": user.token_version})
    refresh_token = generate_refresh_token()

    rt = create_refresh_token_obj(user, refresh_token)
    rt_repo = RefreshTokenRepository(db)
    await rt_repo.create_refresh_token(rt)

    await db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
