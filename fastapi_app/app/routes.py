# app/routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from app.models import TaskCreate, Task
from app.services import TaskService


router = APIRouter()


def get_task_service(request: Request):
    return TaskService(request.app.state.db_pool)


@router.post("/tasks/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(task)


@router.get("/tasks/", response_model=list[Task])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    return await service.list_tasks()


@router.get("/tasks/{task_id}/", response_model=Task)
async def get_task(task_id: str, service: TaskService = Depends(get_task_service)):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}/", response_model=Task)
async def update_task(task_id: str, task: TaskCreate, service: TaskService = Depends(get_task_service)):
    updated = await service.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}/", status_code=204)
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

