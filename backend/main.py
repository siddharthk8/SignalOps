from typing import cast

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ExceptionHandler

from app.api.v1.router import v1_router
from app.core.config import settings
from app.core.exceptions import (
    general_http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.db.core import engine

VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # app runs here
    # shutdown logic
    await engine.dispose()


IS_PRODUCTION = settings.env == "production"

app = FastAPI(
    title="SignalOps",
    description="SignalOps is a log intelligence and incident analysis platform that converts raw system logs into meaningful insights.",
    version=VERSION,
    lifespan=lifespan,
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
)

app.include_router(v1_router, prefix="/api/v1")

# Handle Exceptions
app.add_exception_handler(
    StarletteHTTPException,
    cast(ExceptionHandler, general_http_exception_handler),
)
app.add_exception_handler(
    RequestValidationError,
    cast(ExceptionHandler, validation_exception_handler),
)
app.add_exception_handler(Exception, unhandled_exception_handler)
