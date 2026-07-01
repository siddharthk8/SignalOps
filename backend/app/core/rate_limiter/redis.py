from redis.asyncio import Redis

from app.core.config import settings

# Redis is used as the centralized store for rate-limit buckets.
# The current deployment model is single instance. Update this
# configuration if the deployment architecture changes.
redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True,
)
