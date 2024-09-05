from fastapi import FastAPI

from api.database import init_db
from .routers import router

app = FastAPI()

init_db()

app.include_router(router)
