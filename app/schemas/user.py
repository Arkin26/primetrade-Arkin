from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.db.models.user import UserRole


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value: str) -> str:
        return value.strip().lower()


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserRoleUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: UserRole
