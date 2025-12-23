import datetime
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert,update,select,delete
from fastapi.responses import JSONResponse
from fastapi import HTTPException,Response,Request
from ..databace.databace import engine
from ..models.models import Tasks
from src.schemas.schemas import TaskModel,PatchTask,PutTasksModel,DeleteTask
from enum import Enum




class TaskManager:
    @staticmethod
    async def add_task(request:Request,task_model:TaskModel):

        try:
            user_cookie = request.cookies.get('uuid')
            user_token = jwt.decode(user_cookie,'secret_key',algorithms=['HS256'])
            async with AsyncSession(engine) as session:
                stmt =  insert(Tasks).values(task_model.model_dump()).returning(Tasks.task_text,Tasks.task_title)
                res = await session.execute(stmt)
                row = res.one_or_none()

                await session.commit()
                print(row)
            if row is not None:
                return JSONResponse(status_code=201,content={'status_create':201})
            else:
                raise HTTPException(status_code=400,detail='Попробуйте позже')
        except:
            raise HTTPException(status_code=400,detail='Попробуйте позже')

    @staticmethod
    async def patch_status(request:Request,task_patch:PatchTask):
        try:
            user_cookie = request.cookies.get('uuid')
            user_token = jwt.decode(user_cookie,'secret_key',algorithms=['HS256'])
            async with AsyncSession(engine) as session:
                stmt = update(Tasks).where(Tasks.task_id == task_patch.task_id).values(task_status = task_patch.new_task_status.value)
                res = await session.execute(stmt)
                await session.commit()
            return JSONResponse(status_code=200,content={'status_update':200})
        except Exception as e:
            raise HTTPException(status_code=400,detail='Попробуйте снова')

    @staticmethod
    async def put_task(request:Request,put_task:PutTasksModel):
        try:
            user_cookie = request.cookies.get('uuid')
            user_token = jwt.decode(user_cookie,'secret_key',algorithms=['HS256'])
            async with AsyncSession(engine) as session:
                stmt = update(Tasks).where(Tasks.task_id == put_task.task_id).values(put_task.model_dump())
                res = await session.execute(stmt)
                await session.commit()

            async with AsyncSession(engine) as session:
                stmt = select(Tasks.task_text,Tasks.task_title,Tasks.task_status).where(Tasks.task_id == put_task.task_id)
                res = await session.execute(stmt)
                rows = res.one_or_none()

                if rows is None:
                    raise HTTPException(status_code=400, detail='Попробуйте снова')
                else:
                    return JSONResponse(status_code=200,
                                        content={'status_replace': 200})
            
        except Exception as e:
            raise HTTPException(status_code=400, detail='Попробуйте снова')

    @staticmethod
    async def all_tasks(request:Request):
        try:
            token =  jwt.decode(request.cookies.get('uuid'),'secret_key',algorithms=['HS256'])
            async with AsyncSession(engine) as session:
                stmt = select(Tasks)
                res = await session.execute(stmt)
                rows = res.scalars().all()
                return rows

        except Exception as e:
            raise HTTPException(status_code=400,detail='Попробуйте позже')

    @staticmethod
    async def delete_task(request:Request,task_delete_model:DeleteTask):
        try:
            token = jwt.decode(request.cookies.get('uuid'),'secret_key',algorithms=['HS256'])
            async with AsyncSession(engine) as session:
                stmt = delete(Tasks).where(Tasks.task_id == task_delete_model.task_idm,
                                           Tasks.task_title == task_delete_model.task_title)

                await session.execute(stmt)
                await session.commit()
            return JSONResponse(status_code=200,content={'status_delete':200})
        except Exception as e:
            raise HTTPException(status_code=400,detail='Попробуйте позже')