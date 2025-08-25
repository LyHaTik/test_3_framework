# app/services.py
from app.repositories import TaskRepository


class TaskService:
    def __init__(self, db_pool):
        self.repo = TaskRepository(db_pool)

    async def create_task(self, task):
        return await self.repo.create(task.title, task.description or "", task.status)

    async def list_tasks(self):
        return await self.repo.list_all()

    async def get_task(self, task_id: str):
        return await self.repo.get(task_id)

    async def update_task(self, task_id: str, task):
        return await self.repo.update(task_id, task.title, task.description or "", task.status)

    async def delete_task(self, task_id: str):
        return await self.repo.delete(task_id)


