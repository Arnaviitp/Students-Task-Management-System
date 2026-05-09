from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: str = Field(default="todo", pattern="^(todo|in_progress|done)$")
    priority: int = Field(default=2, ge=1, le=3)
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: str | None = Field(default=None, pattern="^(todo|in_progress|done)$")
    priority: int | None = Field(default=None, ge=1, le=3)
    due_date: datetime | None = None


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

