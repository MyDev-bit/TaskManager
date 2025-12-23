import os

import jwt
from ..schemas.schemas import RegisterModel
from fastapi import Response,Request,status
from ..core import security
from ..services.token_service.token_service import jwt_manager
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from ..databace.databace import engine
from sqlalchemy import insert,select,delete
from sqlalchemy.exc import IntegrityError
from ..models.models import Users
from typing import Annotated
from fastapi import Depends,HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv


load_dotenv('../jwt.env')
secret_key = os.getenv('secret_key')
class UserActions:
    @staticmethod
    async def register_user(reg_model:RegisterModel,response:Response):
        try:
            hash = await  security.create_hash(reg_model.password)
            c_m = reg_model.model_copy(update={"password": hash})
            access_m = jwt_manager.load_token_params(type='access')
            token = access_m.create_access_token(uid=f"{uuid4()}",data=jwt_manager.value_uuid_token(reg_model.name))
            async with AsyncSession(engine) as sess:
                    stmt = insert(Users).values(c_m.model_dump())
                    res = await sess.execute(stmt)
                    await sess.commit()

            response.set_cookie(key='uuid', value=token,httponly=True)
            return {'status_register':'true',
                        'name':c_m.model_dump()['name']}

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Данный пользователь уже существует.')


    @staticmethod
    async def login_user(response:Response,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
        async with AsyncSession(engine) as sess:
            stmt = select(Users.password).where(Users.name == form_data.username)
            res = await sess.execute(stmt)
            row = res.scalar_one_or_none()
        v_data = await security.v_hash(hash_t=row, password=form_data.password)
        match v_data:
            case True:
                access_m = jwt_manager.load_token_params(type='access')
                token = access_m.create_access_token(uid=f'{uuid4()}', data=jwt_manager.value_uuid_token(
                    name=form_data.username))
                response.set_cookie(key='uuid', value=token)
                return {'status_login':'true',
                        'name':form_data.username}

        raise HTTPException(status_code=401,detail='Неверный логин или пароль')


    @staticmethod
    async def log_out(response:Response,request:Request):
        try:
            response.delete_cookie('uuid')
            return JSONResponse(status_code=200,content={'status_logout':200})
        except:
            raise HTTPException(detail='Вы не авторизованы',
                                status_code=status.HTTP_401_UNAUTHORIZED)



    @staticmethod
    async def delete_account(response:Response,request:Request,cookie_name:str):
        try:

            token = jwt.decode(request.cookies.get(cookie_name),secret_key, algorithms=['HS256'])
            print(token)
            async with AsyncSession(engine) as conn:
                    stmt_1 = delete(Users).where(Users.name == token['us_name'])
                    res_1 = await conn.execute(stmt_1)
                    await conn.commit()

                    stmt_2 = select(Users).where(Users.name == token['us_name'])
                    res_2 = await conn.execute(stmt_2)

                    row = res_2.one_or_none()

            response.delete_cookie('uuid',httponly=True)
            if row is  None:
                    return JSONResponse(status_code=200,content={'status_delete':200})

        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Ошибка удаления аккаунта.')



