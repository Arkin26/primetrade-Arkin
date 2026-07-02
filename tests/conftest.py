import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["ADMIN_EMAIL"] = "admin@test.com"
os.environ["ADMIN_PASSWORD"] = "adminpass123"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"
os.environ["TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.core.security import hash_password
from app.db import session as db_session_module
from app.db.base import Base
from app.db.models.user import User, UserRole
from app.db.session import get_db

get_settings.cache_clear()

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_module.engine = engine
db_session_module.SessionLocal = TestingSessionLocal

from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def setup_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        db.add(
            User(
                email="admin@test.com",
                hashed_password=hash_password("adminpass123"),
                role=UserRole.admin,
            )
        )
        db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Session:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def user_credentials() -> dict:
    return {"email": "user@example.com", "password": "password123"}


@pytest.fixture
def registered_user(client: TestClient, user_credentials: dict) -> dict:
    response = client.post("/api/v1/auth/register", json=user_credentials)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def user_headers(registered_user: dict) -> dict:
    token = registered_user["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client: TestClient) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "adminpass123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
