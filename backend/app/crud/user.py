from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Booking, Stock
from app.core.security import hash_password

async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))

async def get_by_username(db: AsyncSession, username: str) -> User | None:
    return await db.scalar(select(User).where(User.username == username))

async def list_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.user_id))
    return list(result.scalars().all())

async def create(db: AsyncSession, data: dict) -> User:
    password = data.pop("password")
    user = User(**data, password_hash=hash_password(password))
    db.add(user)
    await db.flush()

    if user.username is None:
        user.username = f"user{user.user_id}"

    await db.commit()
    await db.refresh(user)
    return user

async def update(db: AsyncSession, user_id: int, data: dict) -> User | None:
    user = await db.get(User, user_id)
    if user is None:
        return None

    if "password" in data and data["password"] is not None:
        user.password_hash = hash_password(data.pop("password"))
    data.pop("password", None)

    for key, value in data.items():
        if value is not None:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete(db: AsyncSession, user_id: int) -> bool:
    user = await db.get(User, user_id)
    if user is None:
        return False

    # release any active bookings before removing the user
    result = await db.execute(select(Booking).where(Booking.user_id == user_id))
    for booking in result.scalars().all():
        if booking.stat in ("pending", "ongoing", "late"):
            stock = await db.scalar(
                select(Stock)
                .where(
                    Stock.book_id == booking.book_id,
                    Stock.loc_id == booking.loc_id,
                )
                .with_for_update()
            )
            if stock:
                stock.available += 1
                stock.reserved -= 1
        await db.delete(booking)

    await db.flush()
    await db.delete(user)
    await db.commit()
    return True
