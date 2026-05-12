from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.api import v1_router
from app.core.exceptions import (
    general_http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

VERSION = "v1"

app = FastAPI(
    title="SignalOps",
    description="SignalOps is a log intelligence and incident analysis platform that converts raw system logs into meaningful insights.",
    version=VERSION,
)

app.include_router(v1_router, prefix="/api/v1")

# Handle Exceptions
app.add_exception_handler(StarletteHTTPException, general_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
