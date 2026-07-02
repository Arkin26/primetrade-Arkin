from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.models.task import TaskStatus


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = TaskStatus.pending

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus | None = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
