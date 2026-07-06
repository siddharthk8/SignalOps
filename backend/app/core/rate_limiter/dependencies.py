from collections.abc import Callable

from fastapi import Request, Response

from app.core.rate_limiter.limiter import rate_limiter
from app.core.rate_limiter.utils import get_client_ip
from app.domains.user.dependencies import CurrentUser


def public_rate_limit(capacity: int, refill_rate: float) -> Callable:
    # Creates a rate limiter dependency for public endpoints using the client's IP address.
    async def dependency(request: Request, response: Response):
        await rate_limiter.check(
            request=request,
            response=response,
            identifier=f"ip:{get_client_ip(request)}",
            capacity=capacity,
            refill_rate=refill_rate,
        )

    return dependency


def user_rate_limit(capacity: int, refill_rate: float) -> Callable:
    # Creates a rate limiter dependency for authenticated endpoints using the user's ID.
    async def dependency(
        request: Request,
        response: Response,
        current_user: CurrentUser,
    ):
        await rate_limiter.check(
            request=request,
            response=response,
            identifier=f"user:{current_user.id}",
            capacity=capacity,
            refill_rate=refill_rate,
        )

    return dependency
