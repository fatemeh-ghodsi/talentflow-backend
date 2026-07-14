from fastapi import (
    Request,
    HTTPException,
    status,
)

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions import AppBaseException
from app.core.logger import logger


async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    if isinstance(exc, AppBaseException):

        logger.warning(
            f"{request.method} {request.url.path} "
            f"{exc.__class__.__name__}: {exc.message}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message,
            },
        )

    if isinstance(exc, RequestValidationError):

        logger.warning(
            f"{request.method} {request.url.path} ValidationError"
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation failed",
                "errors": exc.errors(),
            },
        )

    if isinstance(exc, HTTPException):

        logger.warning(
            f"{request.method} {request.url.path} "
            f"HTTPException: {exc.detail}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    logger.exception(
        f"Unhandled exception on "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred",
        },
    )