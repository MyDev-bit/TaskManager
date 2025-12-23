from fastapi import APIRouter,Request
from fastapi import Response,Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from src.schemas.schemas import RegisterModel
from src.services.user_service import UserActions


users_action = APIRouter(tags=['user_action'])
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


@users_action.post('/register')
async def reg(reg_model:RegisterModel,response:Response):
    return await UserActions.register_user(reg_model, response)




@users_action.post('/login')
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],response:Response):
    return await UserActions.login_user(response, form_data)



@users_action.post('/logout')
async def logout(response:Response,request:Request):
    return await UserActions.log_out(response,request)


@users_action.delete('/delete_account')
async def delete_account(response:Response,request:Request):
    return await UserActions.delete_account(response,request,'uuid')