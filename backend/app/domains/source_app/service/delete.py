from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.source_app import SourceAppRepository
from app.domains.users.dependencies import CurrentUser


async def delete_source_app(source_app_id: int, current_user: CurrentUser, db: Session):
    source_app_repo = SourceAppRepository(db)
    source_app_orm = source_app_repo.get_by_id(source_app_id)

    if source_app_orm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source App does not exists."
        )

    if source_app_orm.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action.",
        )

    source_app_orm = source_app_repo.delete_source_app(source_app_orm)
    db.commit()
