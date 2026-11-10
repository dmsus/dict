from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.db import engine
from app.models import Base
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Создаём таблицы при старте (для продакшна лучше Alembic).
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Словарь (Dictionary) API",
    version="1.0.0",
    description="Сервис «Словарь» — хранение и поиск переводов слов.",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
