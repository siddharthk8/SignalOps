from fastapi import APIRouter

from app.api.v1.endpoints import auth

from .endpoints import events, health, logs

v1_router = APIRouter()

# health
v1_router.include_router(health.router, prefix="/health", tags=["health"])

# others
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
v1_router.include_router(logs.router, prefix="/logs", tags=["logs"])
v1_router.include_router(events.router, prefix="/events", tags=["events"])
