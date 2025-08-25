# app/services.py
import uuid
from .db import get_connection
from .models import Task


def create_task(title: str, description: str) -> Task:
    task_id = str(uuid.uuid4())
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO tasks_task (id, title, description, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, description, status
        """, (task_id, title, description, "создано")
        )
        row = cur.fetchone()
        return Task(**row)


def get_task(task_id: int) -> Task | None:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, description, status
            FROM tasks_task WHERE id = %s
        """, (task_id,))
        row = cur.fetchone()
        return Task(**row) if row else None


def get_all_tasks() -> list[Task]:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, description, status
            FROM tasks_task ORDER BY id
        """)
        rows = cur.fetchall()
        return [Task(**row) for row in rows]


def update_task(task_id: int, title: str, description: str, status: bool) -> Task | None:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE tasks_task SET title = %s, description = %s, status = %s
            WHERE id = %s
            RETURNING id, title, description, status
        """, (title, description, status, task_id)
        )
        row = cur.fetchone()
        return Task(**row) if row else None


def delete_task(task_id: int) -> bool:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            DELETE FROM tasks_task
            WHERE id = %s
        """, (task_id,))
        return cur.rowcount > 0
