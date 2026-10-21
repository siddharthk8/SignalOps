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


# Cases:
# - Existing user with a valid password → login succeeds.
# - Existing user with an incorrect password → 401 Unauthorized.
# - Google-only user with password_hash=None → 401 Unauthorized, without calling verify_password().
# - Inactive user → login fails.
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

    # Google-only users may not have a password. So we need to check for password existence here.
    if not user.password_hash:
        auth_logger.warning(
            "Password authentication failed: no password configured. user_id=%s",
            user.id,
        )
        raise exception

    if not verify_password(form_data.password, user.password_hash):
        auth_logger.warning(
            "Authentication failed: invalid password. user_id=%s",
            user.id,
        )
        raise exception

    if not user.is_active:
        raise exception

    access_token = create_access_token({"sub": str(user.id), "tv": user.token_version})
    refresh_token = generate_refresh_token()

    rt = create_refresh_token_obj(user, refresh_token)
    rt_repo = RefreshTokenRepository(db)
    await rt_repo.save_refresh_token(rt)

    await db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
