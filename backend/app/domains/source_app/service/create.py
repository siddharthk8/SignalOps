from sqlalchemy.orm import Session

from app.db.repositories.source_app import SourceAppRepository
from app.domains.source_app.schemas import SourceAppRequest
from app.domains.users.dependencies import CurrentUser


async def create_source_app(
    data: SourceAppRequest, current_user: CurrentUser, db: Session
):
    source_app_repo = SourceAppRepository(db)
    source_app_orm = source_app_repo.create_source_app(
        user_id=current_user.id, name=data.name, app_type=data.app_type
    )
    db.commit()
    return source_app_orm
