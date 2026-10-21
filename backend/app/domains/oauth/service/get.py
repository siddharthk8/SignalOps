from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.oauth_account import OAuthAccountRepository
from app.domains.oauth.schemas import GetOAuthConnection, GetOAuthConnections
from app.domains.user.dependencies import CurrentUser


async def get_oauth_connections(
    current_user: CurrentUser,
    db: AsyncSession,
) -> GetOAuthConnections:
    oauth_repo = OAuthAccountRepository(db)
    oauth_objects = await oauth_repo.filter_by_user_id(current_user.id)

    if not oauth_objects:
        result = GetOAuthConnections(connections=[])
    else:
        result = GetOAuthConnections(
            connections=[
                GetOAuthConnection(provider=oauth.provider) for oauth in oauth_objects
            ]
        )

    return result
