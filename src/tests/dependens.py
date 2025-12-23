from typing import Annotated

from src.databace.databace import engine

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession



async def engine_di():
    session =    AsyncSession(engine)
    yield session



engine_dep = Annotated[AsyncSession,engine_di]


