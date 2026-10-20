from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.db.engine import engine

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
