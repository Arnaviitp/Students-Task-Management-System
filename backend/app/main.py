from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.crud import create_task, delete_task, get_task, list_tasks, update_task
from app.db import engine, get_db
from app.models import Base
from app.schemas import TaskCreate, TaskOut, TaskUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

print(f"Allowed origins: {settings.allowed_origins_list}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskOut])
def tasks_list(
    q: str | None = None,
    status: str | None = Query(default=None, pattern="^(todo|in_progress|done)$"),
    due_before: datetime | None = None,
    due_after: datetime | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db=Depends(get_db),
):
    return list_tasks(db, q=q, status=status, due_before=due_before, due_after=due_after, skip=skip, limit=limit)


@app.post("/tasks", response_model=TaskOut, status_code=201)
def tasks_create(payload: TaskCreate, db=Depends(get_db)):
    return create_task(db, payload)


@app.get("/tasks/{task_id}", response_model=TaskOut)
def tasks_get(task_id: int, db=Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def tasks_put(task_id: int, payload: TaskCreate, db=Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task, TaskUpdate(**payload.model_dump()))


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def tasks_patch(task_id: int, payload: TaskUpdate, db=Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task, payload)


@app.delete("/tasks/{task_id}", status_code=204)
def tasks_delete(task_id: int, db=Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, task)
    return None

