from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Booking, Stock

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"active", "cancelled"},
    "active": {"overdue", "closed"},
    "overdue": {"closed"},
    "closed": set(),
    "cancelled": set(),
}

RESERVING = {"pending", "active", "overdue"}

def _full(stmt):
    return stmt.options(
        selectinload(Booking.user),
        selectinload(Booking.book),
        selectinload(Booking.location),
    )

async def get_by_id(db: AsyncSession, bk_id: int) -> Booking | None:
    return await db.scalar(
        _full(select(Booking).where(Booking.bk_id == bk_id))
    )

async def list_bookings(
    db: AsyncSession, user_id: int | None = None
) -> list[Booking]:
    stmt = _full(select(Booking).order_by(Booking.bk_id))
    if user_id is not None:
        stmt = stmt.where(Booking.user_id == user_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def create(
    db: AsyncSession,
    user_id: int,
    book_id: int,
    loc_id: int,
    due_days: int = 14,
) -> Booking:
    stock = await db.scalar(
        select(Stock)
        .where(Stock.book_id == book_id, Stock.loc_id == loc_id)
        .with_for_update()
    )
    if stock is None:
        raise ValueError("no stock for this book/location")
    if (stock.available or 0) <= 0:
        raise ValueError("no available copies")

    stock.available -= 1
    stock.reserved = (stock.reserved or 0) + 1

    booking = Booking(
        user_id=user_id,
        book_id=book_id,
        loc_id=loc_id,
        time_created=datetime.now(timezone.utc),
        time_due=datetime.now(timezone.utc) + timedelta(days=due_days),
        stat="pending",
    )
    db.add(booking)
    await db.commit()
    return await get_by_id(db, booking.bk_id)

async def update(
    db: AsyncSession, bk_id: int, data: dict
) -> Booking | None:
    booking = await db.get(Booking, bk_id)
    if booking is None:
        return None

    new_status = data.get("status")
    new_due = data.get("time_due")

    if new_status is not None and new_status != booking.stat:
        allowed = ALLOWED_TRANSITIONS.get(booking.stat, set())
        if new_status not in allowed:
            raise ValueError(
                f"cannot transition {booking.stat} → {new_status}"
            )

        stock = await db.scalar(
            select(Stock)
            .where(
                Stock.book_id == booking.book_id,
                Stock.loc_id == booking.loc_id,
            )
            .with_for_update()
        )

        if new_status in ("closed", "cancelled") and booking.stat in RESERVING:
            if stock:
                stock.available = (stock.available or 0) + 1
                stock.reserved = max(0, (stock.reserved or 0) - 1)
            if new_status == "closed":
                booking.time_closed = datetime.now(timezone.utc)

        booking.stat = new_status

    if new_due is not None:
        booking.time_due = new_due

    await db.commit()
    return await get_by_id(db, bk_id)

async def delete(db: AsyncSession, bk_id: int) -> bool:
    booking = await db.get(Booking, bk_id)
    if booking is None:
        return False

    if booking.stat in RESERVING:
        stock = await db.scalar(
            select(Stock)
            .where(
                Stock.book_id == booking.book_id,
                Stock.loc_id == booking.loc_id,
            )
            .with_for_update()
        )
        if stock:
            stock.available = (stock.available or 0) + 1
            stock.reserved = max(0, (stock.reserved or 0) - 1)

    await db.delete(booking)
    await db.commit()
    return True
