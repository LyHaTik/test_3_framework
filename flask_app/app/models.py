# app/models.py
from dataclasses import dataclass, field
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.CREATED

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
        }

