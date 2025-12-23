from fastapi import Response
from src.services.token_service.token_service import access_token_m


class TestRouter:
    @staticmethod
    async def set_root_cookie(response:Response,cookie_name:str):
        root_token = access_token_m.create_access_token(uid='test')
        response.set_cookie(key=cookie_name, value=root_token)
        return {'status':'true'}

    @staticmethod
    async def del_root_cookie(response:Response,cookie_name:str):
        response.delete_cookie(cookie_name)
        return {'status':'true'}