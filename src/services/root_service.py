from src.databace.databace import engine
from src.models.models import Base,Users
from src.dinamic_schemas.schemas import model_2
from sqlalchemy import select,func,insert,delete
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import psutil
from fastapi import Request,HTTPException,status,Response
from fastapi.responses import JSONResponse


class RootActions:
    @staticmethod
    async def check_db(request:Request):
        try:
            root_cookie = request.cookies.get('r_uuid_s')
            root_token = jwt.decode(root_cookie, 'secret_key', algorithms=['HS256'])
            async with AsyncSession(engine) as sess_1:
                stmt_1 = insert(Users).values({'name':'test','password':'test'})
                await sess_1.execute(stmt_1)
                await sess_1.commit()

            async with AsyncSession(engine) as session_2:
                stmt_2 = select(Users).where(Users.name == 'test')
                res = await session_2.execute(stmt_2)
                row = res.one_or_none()
            if row is not None:
                async with AsyncSession(engine) as session_3:
                    stmt_3 = delete(Users).where(Users.name == 'test')
                    await session_3.execute(stmt_3)
                    await session_3.commit()

                return Response(status_code=200)
            else:
                raise HTTPException(status_code=400)

        except Exception as e:
            raise HTTPException(status_code=400)
    @staticmethod
    async def create_db(request:Request):
        try:
            root_cookie = request.cookies.get('r_uuid_s')
            root_token = jwt.decode(root_cookie, 'secret_key', algorithms=['HS256'])
            async with engine.begin() as sess:
                await sess.run_sync(Base.metadata.create_all)
            return JSONResponse(status_code=201,content={'status_create':201})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Попробуйте позже')


    @staticmethod
    async def root_patch(request:Request):
        root_cookie = request.cookies.get('r_uuid_s')
        print(type(root_cookie))
        if root_cookie is not None:
            root_token = jwt.decode(root_cookie,'secret_key', algorithms=['HS256'])
            if root_token:
                async with AsyncSession(engine) as sess:
                    stmt_1 = select(func.max(Users.id))
                    res = await sess.execute(stmt_1)
                    row =  res.one_or_none()

            return {"количество_п":f"{max(row)}",
                    'процент используемой памяти':f"{psutil.virtual_memory().percent}",
                    'свободное место':f"{psutil.virtual_memory().available / 1024}"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='У вас нет доступа')


root_actions = RootActions()