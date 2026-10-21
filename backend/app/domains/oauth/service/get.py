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

    print("User ID:", current_user.id)
    print("User Name:", current_user.first_name)
    print("OAuth objects:", oauth_objects)

    if oauth_objects:
        for oauth in oauth_objects:
            print("ID:", oauth.id)
            print("User ID:", oauth.user_id)
            print("Provider:", oauth.provider)
            print("Google Sub ID:", oauth.provider_user_id)

    if not oauth_objects:
        result = GetOAuthConnections(connections=[])
    else:
        result = GetOAuthConnections(
            connections=[
                GetOAuthConnection(provider=oauth.provider) for oauth in oauth_objects
            ]
        )

    # Print the actual response schema
    print("Returning OAuth connections:", result)

    # Print as JSON for easier debugging
    print("Returning JSON:", result.model_dump_json(indent=2))

    return result
