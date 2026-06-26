from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.source_app import SourceAppRepository
from app.domains.source_app.schemas import SourceAppModel, SourceAppRequest
from app.domains.users.dependencies import CurrentUser


async def create_source_app(
    data: SourceAppRequest, current_user: CurrentUser, db: AsyncSession
):
    source_app_repo = SourceAppRepository(db)
    source_app = await source_app_repo.create_source_app(
        user_id=current_user.id, name=data.name, app_type=data.app_type
    )
    response = SourceAppModel.model_validate(source_app)
    await db.commit()
    return response
