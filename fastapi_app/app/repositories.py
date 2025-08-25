# app/repositories.py
import uuid


class TaskRepository:
    def __init__(self, db_pool):
        self.pool = db_pool

    async def create(self, title: str, description: str, status: str) -> dict:
        task_id = str(uuid.uuid4())
        query = """
            INSERT INTO tasks_task (id, title, description, status)
            VALUES ($1, $2, $3, $4)
            RETURNING id, title, description, status
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, task_id, title, description, status)
        return {**dict(row), "id": str(row["id"])}

    async def list_all(self) -> list[dict]:
        query = """
            SELECT id, title, description, status
            FROM tasks_task
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [{**dict(row), "id": str(row["id"])} for row in rows]

    async def get(self, task_id: str) -> dict | None:
        query = """
            SELECT id, title, description, status
            FROM tasks_task
            WHERE id=$1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, task_id)
        return {**dict(row), "id": str(row["id"])} if row else None

    async def update(self, task_id: str, title: str, description: str, status: str) -> dict | None:
        query = """
            UPDATE tasks_task
            SET title=$1, description=$2, status=$3
            WHERE id=$4
            RETURNING id, title, description, status
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, title, description, status, task_id)
        return {**dict(row), "id": str(row["id"])} if row else None

    async def delete(self, task_id: str) -> bool:
        query = """
                DELETE FROM tasks_task
                WHERE id=$1
        """
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, task_id)
        return result.endswith("1")
