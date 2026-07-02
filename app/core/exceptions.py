from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ErrorDetail, ErrorResponse


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: list[dict] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


def _error_payload(code: str, message: str, details: list[dict] | None = None) -> dict:
    return ErrorResponse(error=ErrorDetail(code=code, message=message, details=details)).model_dump()


async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(exc.code, exc.message, exc.details),
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        {
            "field": ".".join(str(loc) for loc in err.get("loc", [])),
            "message": err.get("msg", "Invalid value"),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=_error_payload("VALIDATION_ERROR", "Request validation failed", details),
    )


async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = "UNAUTHORIZED" if exc.status_code == 401 else "HTTP_ERROR"
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(code, str(exc.detail)),
    )


async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=_error_payload("INTERNAL_ERROR", "An unexpected error occurred"),
    )
