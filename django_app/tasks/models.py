# tasks/models.py
import uuid
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        CREATED = "создано"
        IN_PROGRESS = "в работе"
        COMPLETED = "завершено"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }
