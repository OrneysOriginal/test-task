from fastapi import FastAPI
from contextlib import asynccontextmanager

from analytics.router import analytics_router
from database import create_table, delete_table
from user.router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_table()
    await create_table()
    print('On')
    yield
    print('Off')


app = FastAPI(lifespan=lifespan)

app.include_router(
    analytics_router,
)

app.include_router(
    user_router,
)
