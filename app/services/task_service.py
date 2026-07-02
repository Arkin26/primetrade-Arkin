import math
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.db.models.task import Task, TaskStatus
from app.db.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate


def _can_access_task(user: User, task: Task) -> bool:
    return user.role == UserRole.admin or task.owner_id == user.id


def create_task(db: Session, user: User, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        owner_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, user: User, task_id: UUID) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise AppException("NOT_FOUND", "Task not found", status_code=404)
    if not _can_access_task(user, task):
        raise AppException("FORBIDDEN", "Not allowed to access this task", status_code=403)
    return task


def list_tasks(
    db: Session,
    user: User,
    *,
    page: int = 1,
    limit: int = 20,
    owner_id: UUID | None = None,
    status: TaskStatus | None = None,
    sort: str = "-created_at",
) -> tuple[list[Task], int]:
    query = select(Task)

    if user.role == UserRole.admin:
        if owner_id is not None:
            query = query.where(Task.owner_id == owner_id)
    else:
        query = query.where(Task.owner_id == user.id)

    if status is not None:
        query = query.where(Task.status == status)

    if sort.startswith("-"):
        sort_field = sort[1:]
        descending = True
    else:
        sort_field = sort
        descending = False

    sort_column = getattr(Task, sort_field, None)
    if sort_column is None:
        sort_column = Task.created_at
        descending = True

    query = query.order_by(sort_column.desc() if descending else sort_column.asc())

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * limit
    tasks = list(db.scalars(query.offset(offset).limit(limit)).all())
    return tasks, total


def update_task(db: Session, user: User, task_id: UUID, data: TaskUpdate) -> Task:
    task = get_task(db, user, task_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user: User, task_id: UUID) -> None:
    task = get_task(db, user, task_id)
    db.delete(task)
    db.commit()


def paginate_meta(total: int, page: int, limit: int) -> dict:
    pages = math.ceil(total / limit) if total else 0
    return {"total": total, "page": page, "limit": limit, "pages": pages}
