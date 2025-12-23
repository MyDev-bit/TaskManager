from fastapi import APIRouter,Response,Request,Form,status
from src.services.task_manager import TaskManager
from src.schemas.schemas import TaskModel,PatchTask,PutTasksModel,DeleteTask
from typing import Annotated

tasks_router = APIRouter(tags=['tasks'])


@tasks_router.post('/add_task',status_code=201)
async def add_task(request:Request,task_model:Annotated[TaskModel,Form()]):
    return await TaskManager.add_task(request, task_model)



@tasks_router.patch('/patch_task_status/{new_status}',status_code=status.HTTP_200_OK)
async def patch_task(request:Request,task_patch:Annotated[PatchTask,Form()]):
    return await TaskManager.patch_status(request, task_patch)


@tasks_router.put('/put_task/{task_id}',status_code=200)
async def put_task(request:Request,task_put:Annotated[PutTasksModel,Form()]):
    return await TaskManager.put_task(request,task_put)

@tasks_router.get('/all_tasks',status_code=200)
async def all_tasks(request:Request):
    return await TaskManager.all_tasks(request)


@tasks_router.delete('/delete_task')
async def delete_task(request:Request,task_delete_model:DeleteTask):
    return await TaskManager.delete_task(request,task_delete_model)
