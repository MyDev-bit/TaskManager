from fastapi import APIRouter,Request
from src.services.root_service import RootActions

root_router = APIRouter(tags=['root_router'])


@root_router.get('/')
async def root_patch(request:Request):
    return await RootActions.root_patch(request)


@root_router.post('/create_db',status_code=201)
async def create_db(request:Request):
    return await RootActions.create_db(request)

@root_router.head('/check_db')
async def check_db(request:Request):
    return await RootActions.check_db(request)