from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def general_http_exception_handler(
    _request: Request,
    exception: StarletteHTTPException,
):
    message = "Something went wrong."
    if exception.detail:
        message = exception.detail

    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": message},
    )


async def validation_exception_handler(
    _request: Request,
    exception: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exception.errors()},
    )


# Global fallback handler (catch-all)
async def unhandled_exception_handler(_request: Request, _exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
