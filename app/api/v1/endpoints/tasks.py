from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.deps import AdminUser, CurrentUser, DbSession
from app.db.models.task import TaskStatus
from app.schemas.common import PaginatedResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.user import UserResponse, UserRoleUpdate
from app.services import auth_service, task_service

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=PaginatedResponse[TaskResponse])
def list_tasks(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    owner_id: UUID | None = None,
    status: TaskStatus | None = None,
    sort: str = Query("-created_at"),
) -> PaginatedResponse[TaskResponse]:
    tasks, total = task_service.list_tasks(
        db,
        current_user,
        page=page,
        limit=limit,
        owner_id=owner_id,
        status=status,
        sort=sort,
    )
    meta = task_service.paginate_meta(total, page, limit)
    return PaginatedResponse[TaskResponse](
        items=[TaskResponse.model_validate(task) for task in tasks],
        **meta,
    )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: DbSession, current_user: CurrentUser) -> TaskResponse:
    task = task_service.create_task(db, current_user, data)
    return TaskResponse.model_validate(task)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: DbSession, current_user: CurrentUser) -> TaskResponse:
    task = task_service.get_task(db, current_user, task_id)
    return TaskResponse.model_validate(task)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    data: TaskUpdate,
    db: DbSession,
    current_user: CurrentUser,
) -> TaskResponse:
    task = task_service.update_task(db, current_user, task_id, data)
    return TaskResponse.model_validate(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: DbSession, current_user: CurrentUser) -> None:
    task_service.delete_task(db, current_user, task_id)


@router.get("/users", response_model=list[UserResponse])
def list_users(db: DbSession, _admin: AdminUser) -> list[UserResponse]:
    users = auth_service.list_users(db)
    return [UserResponse.model_validate(user) for user in users]


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: UUID,
    data: UserRoleUpdate,
    db: DbSession,
    _admin: AdminUser,
) -> UserResponse:
    user = auth_service.update_user_role(db, user_id, data.role)
    return UserResponse.model_validate(user)
