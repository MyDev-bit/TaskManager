
from fastapi import FastAPI,Request
from src.routers.UserAction import router_1
from src.routers.RootRouter import router_2
from src.routers.TestRouter import router_3
from src.routers.TasksRouter import router_4
import uvicorn

app = FastAPI(title='TaskManager')
app.include_router(router_1.users_action)
app.include_router(router_2.root_router)
app.include_router(router_3.test_router)
app.include_router(router_4.tasks_router)






if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0')