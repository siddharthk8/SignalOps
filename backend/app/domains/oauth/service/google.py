from functools import partial

from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.oauth_account import OAuthAccountRepository
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.schemas import TokenResponse
from app.domains.auth.utils import (
    create_access_token,
    create_refresh_token_obj,
    generate_refresh_token,
)
from app.domains.oauth.schemas import GoogleLoginRequest


async def google_login(data: GoogleLoginRequest, db: AsyncSession):
    try:
        google_user = await run_in_threadpool(
            partial(
                id_token.verify_oauth2_token,
                data.credential,
                google_requests.Request(),
                settings.google_client_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Google credential",
        ) from exc

    google_sub = google_user.get("sub")
    email = google_user.get("email")
    email_verified = google_user.get("email_verified") is True

    first_name = google_user.get("given_name") or "Google"
    last_name = google_user.get("family_name") or "User"

    if not google_sub or not email or not email_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A verified Google email is required",
        )

    oauth_repo = OAuthAccountRepository(db)
    user_repo = UserRepository(db)

    try:
        oauth_account = await oauth_repo.get_google_oauth_by_provider_user_id(
            google_sub
        )

        if oauth_account is not None:
            # Trust the existing OAuth link, not an email lookup.
            user = await user_repo.get_by_id(oauth_account.user_id)

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        else:
            user = await user_repo.get_by_email(email)

            if user is not None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Google sign-in is not enabled for your account. "
                        "Sign in with your email and password, then enable "
                        "Google sign-in in your account settings."
                    ),
                )

            user = await user_repo.save_google_user(
                email,
                first_name,
                last_name,
            )
            await oauth_repo.save_for_google(
                user_id=user.id,
                sub_id=google_sub,
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "tv": user.token_version,
            }
        )

        refresh_token = generate_refresh_token()
        rt = create_refresh_token_obj(user, refresh_token)

        rt_repo = RefreshTokenRepository(db)
        await rt_repo.save_refresh_token(rt)

        await db.commit()
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except Exception:
        await db.rollback()
        raise
