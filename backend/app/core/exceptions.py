from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def general_http_exception_handler(
    _request: Request,
    exception: StarletteHTTPException,
):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "message": str(exception.detail),
        },
    )


async def validation_exception_handler(
    _request: Request,
    exception: RequestValidationError,
):
    errors = []

    for error in exception.errors():
        errors.append(
            {
                "field": error["loc"][-1],
                "error": error["msg"],
            }
        )

    print(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "message": "Validation failed",
            "errors": errors,
        },
    )


# Global fallback handler (catch-all)
async def unhandled_exception_handler(
    _request: Request,
    _exception: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
        },
    )
