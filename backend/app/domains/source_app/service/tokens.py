from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.source_app import SourceAppRepository
from app.domains.source_app.schemas import (
    SourceAppAccessTokenGenerationResponse,
    SourceAppAccessTokenRequest,
)
from app.domains.source_app.utils import (
    generate_access_key,
    generate_secret_access_key,
    get_source_app_hashed_secret_access_key,
)
from app.domains.user.dependencies import CurrentUser


async def generate_source_app_access_token(
    data: SourceAppAccessTokenRequest, current_user: CurrentUser, db: AsyncSession
):
    access_key = generate_access_key()
    secret_access_key = generate_secret_access_key()
    secret_access_key_hash = get_source_app_hashed_secret_access_key(secret_access_key)

    source_app_repo = SourceAppRepository(db)
    source_app = await source_app_repo.get_by_id(data.source_app_id)

    if source_app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source app does not exists."
        )

    if source_app.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )

    await source_app_repo.update_source_app_access_token(
        access_key, secret_access_key_hash, source_app.id, current_user.id
    )

    final_access_token = access_key + "." + secret_access_key
    await db.commit()

    return SourceAppAccessTokenGenerationResponse(access_token=final_access_token)


async def delete_source_app_access_token(
    data: SourceAppAccessTokenRequest, current_user: CurrentUser, db: AsyncSession
):
    source_app_repo = SourceAppRepository(db)
    source_app = await source_app_repo.get_by_id(data.source_app_id)

    if source_app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source app does not exists."
        )

    if source_app.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )

    await source_app_repo.update_source_app_access_token(
        None, None, source_app.id, current_user.id
    )
    await db.commit()
