from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    batches,
    dashboard,
    incidents,
    logs,
    root,
    source_apps,
    users,
)

v1_router = APIRouter()

v1_router.include_router(root.router, prefix="", tags=["root"])

# others
v1_router.include_router(
    source_apps.router, prefix="/source-apps", tags=["source-apps"]
)
v1_router.include_router(batches.router, prefix="/batches", tags=["batches"])
v1_router.include_router(users.router, prefix="/users", tags=["users"])
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
v1_router.include_router(logs.router, prefix="/logs", tags=["logs"])
v1_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
v1_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
