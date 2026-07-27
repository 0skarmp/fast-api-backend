import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common.config import get_settings
from app.data.database import database_is_configured, init_database
from app.routes.auth_routes import router as auth_router
from app.routes.task_routes import router as task_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if database_is_configured():
        await asyncio.to_thread(init_database)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.app_debug,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "API funcionando",
        "environment": settings.app_env,
    }
