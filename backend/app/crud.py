from __future__ import annotations

from datetime import datetime

from sqlalchemy import Select, asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskUpdate


def _status_from_str(value: str) -> TaskStatus:
    return TaskStatus(value)


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(
        title=data.title.strip(),
        description=(data.description.strip() if isinstance(data.description, str) else data.description),
        status=_status_from_str(data.status),
        priority=data.priority,
        due_date=data.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def list_tasks(
    db: Session,
    *,
    q: str | None = None,
    status: str | None = None,
    due_before: datetime | None = None,
    due_after: datetime | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Task]:
    stmt: Select[tuple[Task]] = select(Task)

    if q:
        query = f"%{q.strip()}%"
        stmt = stmt.where(or_(Task.title.ilike(query), Task.description.ilike(query)))

    if status:
        stmt = stmt.where(Task.status == _status_from_str(status))

    if due_before:
        stmt = stmt.where(Task.due_date.is_not(None)).where(Task.due_date <= due_before)

    if due_after:
        stmt = stmt.where(Task.due_date.is_not(None)).where(Task.due_date >= due_after)

    # Sort: earliest due first, nulls last; then newest created
    nulls_last_due = asc(func.coalesce(Task.due_date, datetime.max))
    stmt = stmt.order_by(nulls_last_due, desc(Task.created_at)).offset(skip).limit(min(limit, 200))
    return list(db.scalars(stmt).all())


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    fields = data.model_fields_set

    if "title" in fields and data.title is not None:
        task.title = data.title.strip()
    if "description" in fields:
        task.description = data.description.strip() if isinstance(data.description, str) else data.description
    if "status" in fields and data.status is not None:
        task.status = _status_from_str(data.status)
    if "priority" in fields and data.priority is not None:
        task.priority = data.priority
    if "due_date" in fields:
        task.due_date = data.due_date

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
