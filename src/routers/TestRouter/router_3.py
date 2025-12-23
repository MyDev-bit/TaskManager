from fastapi import APIRouter,Response
from src.services.test_servise_router import TestRouter

test_router = APIRouter(tags=['tests'],deprecated=False)



@test_router.post('/tests/dev/root_token/set_token',summary='Set root token',status_code=201)
async def set_root(response:Response):
    return await TestRouter.set_root_cookie(response,'r_uuid_s')


@test_router.delete('/tests/dev/root_token/delete_token',
                    status_code=200,
                    summary='Delete root token')
async def set_root(response:Response):
    return await TestRouter.del_root_cookie(response,cookie_name='r_uuid_s')


@test_router.get('/ping')
async def test():
    return 'pong'