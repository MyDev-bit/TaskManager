from pydantic import BaseModel,Field,field_validator
from enum import Enum
import datetime
from fastapi import HTTPException
from typing import Annotated, Any, Self


class TaskStats(str, Enum):
    created = 'created'              # задача создана, но ещё не запущена
    queued = 'queued'                # стоит в очереди на выполнение
    assigned = 'assigned'            # назначена исполнителю
    in_progress = 'in_progress'      # выполняется
    on_hold = 'on_hold'              # приостановлена (ожидание чего-то)
    retrying = 'retrying'            # повторная попытка выполнения
    under_review = 'under_review'    # на проверке / ревью
    complete = 'complete'            # успешно выполнена
    failed = 'failed'                # завершилась ошибкой
    canceled = 'canceled'            # отменена пользователем или системой

class TaskModel(BaseModel):
    task_status: TaskStats
    task_title: str
    task_text: str
    task_time_start: datetime.date = Field(default=datetime.date)
    task_time_end:datetime.date = Field(default=datetime.date)


class PutTasksModel(TaskModel):
    task_id:int

class DeleteTask(BaseModel):
    task_id:int
    task_title:str


class PatchTask(BaseModel):
    task_id:int
    new_task_status:TaskStats



class RegisterModel(BaseModel):
    name:str
    password:str

    @field_validator('name',mode='before')
    def validate(cls, value: str):
        if value == 'test':
            raise HTTPException(423,detail='Данный ник запрещен')
        return value