from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin


def register_user(db: Session, data: UserCreate) -> tuple[User, str]:
    existing = db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise AppException("CONFLICT", "Email already registered", status_code=409)

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.user,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, user.role.value)
    return user, token


def login_user(db: Session, data: UserLogin) -> str:
    user = db.scalar(select(User).where(User.email == data.email))
    if user is None or not verify_password(data.password, user.hashed_password):
        raise AppException("INVALID_CREDENTIALS", "Invalid email or password", status_code=401)
    if not user.is_active:
        raise AppException("FORBIDDEN", "Inactive user account", status_code=403)
    return create_access_token(user.id, user.role.value)


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


def update_user_role(db: Session, user_id, role: UserRole) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise AppException("NOT_FOUND", "User not found", status_code=404)
    user.role = role
    db.commit()
    db.refresh(user)
    return user
