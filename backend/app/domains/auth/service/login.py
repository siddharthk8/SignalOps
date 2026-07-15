from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import auth_logger
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.schemas import TokenResponse
from app.domains.auth.utils import (
    create_access_token,
    create_refresh_token_obj,
    generate_refresh_token,
    verify_password,
)


async def create_token(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = form_data.username
    user = await UserRepository(db).get_by_email(email)

    if not user:
        raise exception

    if not verify_password(form_data.password, user.password_hash):
        auth_logger.warning(
            "Authentication failed: invalid password. user_id=%s",
            user.id,
        )
        raise exception

    access_token = create_access_token({"sub": str(user.id), "tv": user.token_version})
    refresh_token = generate_refresh_token()

    rt = create_refresh_token_obj(user, refresh_token)
    rt_repo = RefreshTokenRepository(db)
    await rt_repo.save_refresh_token(rt)

    await db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
