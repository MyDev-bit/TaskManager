import os
from datetime import timedelta
import datetime

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException,status
from authx import AuthX,AuthXConfig

class JWTManager:

    types_jwt = {'access': 20,
                 'refresh': 30}

    def __init__(self,secret_key:str):
        self.secret_key = secret_key

    def value_uuid_token(self,name:str):
        return {'us_name':name,
               'r_time':f'{datetime.date.today()}'}


    def load_token_params(self,type:str) :
        auth_x_c = AuthXConfig()
        auth_x_c.JWT_TOKEN_LOCATION = ['cookies']
        auth_x_c.JWT_SECRET_KEY =self.secret_key
        auth_x_c.JWT_COOKIE_HTTP_ONLY = True
        try:
            auth_x_c.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=jwt_manager.types_jwt[type])
            auth_x_c.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=jwt_manager.types_jwt[type])
            secret = AuthX(auth_x_c)
            return secret
        except KeyError:
            raise HTTPException(status_code=500,
                                detail='Ошибка сервера.')



load_dotenv('../../jwt.env')
jwt_manager = JWTManager(os.getenv('secret_key'))
refresh_t_manager =  jwt_manager.load_token_params(type='refresh')
access_token_m = jwt_manager.load_token_params(type='access')