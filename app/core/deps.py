from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.db.models.user import User, UserRole
from app.db.session import get_db

security = HTTPBearer(auto_error=False)

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppException("UNAUTHORIZED", "Not authenticated", status_code=401)

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload.get("sub", ""))
    except (JWTError, ValueError, TypeError):
        raise AppException("UNAUTHORIZED", "Invalid or expired token", status_code=401)

    user = db.get(User, user_id)
    if user is None:
        raise AppException("UNAUTHORIZED", "User not found", status_code=401)
    if not user.is_active:
        raise AppException("FORBIDDEN", "Inactive user account", status_code=403)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.admin:
        raise AppException("FORBIDDEN", "Admin access required", status_code=403)
    return current_user


AdminUser = Annotated[User, Depends(require_admin)]
