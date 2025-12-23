from pytest_asyncio import fixture
from src.tests.dependens import engine_dep
from src.models.models import Base

@fixture(scope='session')
async def create_table(engine:engine_dep):
        await engine.begin()
        await engine.run_sync(Base.metadata.create_all)
        await engine.commit()
        await engine.close()
        yield engine

        await engine.begin()
        await engine.run_sync(Base.metadata.drop_all)
        await engine.commit()
        await engine.close()