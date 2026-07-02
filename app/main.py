import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.security import hash_password
from app.db.models.user import User, UserRole
from app.db.session import SessionLocal

settings = get_settings()

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("primetrade")


def seed_admin_user() -> None:
    with SessionLocal() as db:
        admin = db.scalar(select(User).where(User.email == settings.ADMIN_EMAIL))
        if admin is None:
            db.add(
                User(
                    email=settings.ADMIN_EMAIL,
                    hashed_password=hash_password(settings.ADMIN_PASSWORD),
                    role=UserRole.admin,
                )
            )
            db.commit()
            logger.info("Seeded default admin user")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not os.getenv("TESTING"):
        seed_admin_user()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Scalable REST API with JWT authentication and role-based access control.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response

    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/health/ready", tags=["health"])
    def health_ready() -> dict:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}

    return app


app = create_app()
