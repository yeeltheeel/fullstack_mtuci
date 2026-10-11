from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserOut


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    return (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(
        username=data.username,
        birthday=data.birthday,
        email=data.email,
        avatar=data.avatar,
        pass_=hash_password(data.pass_),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def to_user_out(user: User, *, logged: bool = True) -> UserOut:
    return UserOut(
        user_id=user.user_id,
        username=user.username,
        birthday=user.birthday,
        email=user.email,
        avatar=user.avatar,
        logged=logged,
    )