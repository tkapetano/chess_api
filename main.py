import fastapi
import uvicorn

from sql_app import sql_access
from views import home

api = fastapi.FastAPI()


def configure():
    api.include_router(home.router)
    api.include_router(sql_access.router)


configure()
if __name__ == '__main__':
    uvicorn.run(api)
