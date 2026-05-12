from fastapi import FastAPI
from app.api.v1.api import v1_router

VERSION = "v1"

app = FastAPI(
    title="SignalOps",
    description="SignalOps is a log intelligence and incident analysis platform that converts raw system logs into meaningful insights.",
    version=VERSION,
)

app.include_router(v1_router, prefix="/api/v1")
