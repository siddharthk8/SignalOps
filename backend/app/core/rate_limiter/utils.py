from ipaddress import ip_address

from fastapi import Request


def get_client_ip(request: Request) -> str:
    """
    Return the real client IP or unknown.
    """

    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        # X-Forwarded-For: client, proxy1, ...
        ip = forwarded_for.split(",", 1)[0].strip()
    elif request.client:
        # Fallback if the reverse proxy (Nginx) isn't configured.
        ip = request.client.host
    else:
        return "unknown"

    try:
        # Normalize IPv4/IPv6 to a canonical/standard representation.
        return str(ip_address(ip))
    except ValueError:
        # Invalid IP address.
        return "unknown"


def get_route_key(request: Request) -> str:
    """
    Return a stable route identifier.

    Examples:
        path:/users/{id}  # instead of path:/users/1
        path:/login
    """

    # Prefer the route template instead of the actual URL.
    route = request.scope.get("route")
    if route:
        return f"path:{route.path}"

    # Fallback
    path = request.url.path.rstrip("/") or "/"
    return f"path:{path}"
