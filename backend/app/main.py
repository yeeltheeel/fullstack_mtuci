from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.db.base import Base
from app.db.session import engine
import app.db.models  # noqa: register models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # replace with alembic later
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Library API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"status": "ok"}