from fastapi import APIRouter

from app.api.v1.endpoints import auth

from .endpoints import batch, health, logs, source_apps, users

v1_router = APIRouter()

# health
v1_router.include_router(health.router, prefix="/health", tags=["health"])

# others
v1_router.include_router(
    source_apps.router, prefix="/source-apps", tags=["source-apps"]
)
v1_router.include_router(batch.router, prefix="/batch", tags=["batch"])
v1_router.include_router(users.router, prefix="/users", tags=["users"])
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
v1_router.include_router(logs.router, prefix="/logs", tags=["logs"])
