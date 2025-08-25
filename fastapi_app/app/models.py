# app/models.py
from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class TaskCreate(BaseModel):
    title: str
    description: str | None = ""
    status: TaskStatus | None = TaskStatus.CREATED


class Task(TaskCreate):
    id: str

