from fastapi import APIRouter, status

from app.core.deps import CurrentUser, DbSession
from app.schemas.auth import RegisterResponse, TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DbSession) -> RegisterResponse:
    user, token = auth_service.register_user(db, data)
    return RegisterResponse(user=UserResponse.model_validate(user), access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: DbSession) -> TokenResponse:
    token = auth_service.login_user(db, data)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)
