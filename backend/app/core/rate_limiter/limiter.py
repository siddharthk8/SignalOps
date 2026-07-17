import time

from fastapi import HTTPException, Request, Response, status
from redis.asyncio import Redis

from app.core.config import settings

from .redis import redis_client
from .utils import get_route_key


class RedisRateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def _get_redis_key(self, identifier: str, route: str) -> str:
        return f"rate:{identifier}:{route}"

    async def allow(
        self,
        identifier: str,
        route: str,
        capacity: float,
        refill_rate: float,
    ) -> bool:

        key = self._get_redis_key(identifier, route)
        now = time.time()  # Unix time

        # fetch current bucket state
        data = await self.redis.hgetall(key)

        if not data:
            # initialize bucket
            tokens = capacity
            last_refill = now
        else:
            # using float values in tokens, allows smooth refilling.
            tokens = float(data["tokens"])
            last_refill = float(data["last_refill"])

        # refill logic
        seconds_elapsed = now - last_refill
        tokens = min(capacity, tokens + seconds_elapsed * refill_rate)

        # decision
        if tokens < 1:
            # persist updated state
            await self.redis.hset(
                key,
                mapping={
                    "tokens": tokens,
                    "last_refill": now,
                },
            )
            # If a user never comes back, Redis will automatically deletes the bucket after one hour.
            # Without this, millions of inactive users would accumulate.
            await self.redis.expire(key, 3600)  # cleanup old keys
            return False

        # consume token
        tokens -= 1

        await self.redis.hset(
            key,
            mapping={
                "tokens": tokens,
                "last_refill": now,
            },
        )
        await self.redis.expire(key, 3600)
        return True


class RateLimiter:
    def __init__(self, redis_client: Redis):
        self._limiter = RedisRateLimiter(redis_client)

    async def check(
        self,
        *,
        request: Request,
        response: Response,
        identifier: str,
        capacity: float,
        refill_rate: float,
    ) -> None:
        # Disable rate limiting in the test environment.
        if settings.testing or settings.env == "development":
            return

        route = get_route_key(request)

        allowed = await self._limiter.allow(
            identifier=identifier,
            route=route,
            capacity=capacity,
            refill_rate=refill_rate,
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests.",
                headers={"Retry-After": "1"},
            )

        response.headers["X-RateLimit-Limit"] = str(capacity)


rate_limiter = RateLimiter(redis_client)
