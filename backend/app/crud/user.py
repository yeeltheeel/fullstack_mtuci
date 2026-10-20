from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.core.security import hash_password

async def get_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)

async def create(db: AsyncSession, username: str, password: str) -> User:
    user = User(username=username, hashed_password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def list_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.user_id))
    return list(result.scalars().all())
