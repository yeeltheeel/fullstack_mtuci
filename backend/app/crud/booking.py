from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Booking, Book, Stock
from app.schemas.booking import BookingCreate, BookingOut
from app.schemas.location import LocationOut
from app.schemas.user import UserOut
from app.crud.book import to_book_out


_FULL_LOAD = (
    selectinload(Booking.user),
    selectinload(Booking.location),
    selectinload(Booking.book).selectinload(Book.stock).selectinload(Stock.location),
)


def to_booking_out(b: Booking) -> BookingOut:
    return BookingOut(
        bk_id=b.bk_id,
        user=UserOut.model_validate(b.user),
        book=to_book_out(b.book),
        location=LocationOut.model_validate(b.location),
        time_created=b.time_created,
        time_due=b.time_due,
        time_closed=b.time_closed,
        stat=b.stat,
    )


async def create_booking(db: AsyncSession, user_id: int, data: BookingCreate) -> BookingOut:
    stmt = (
        select(Stock)
        .where(Stock.book_id == data.book_id, Stock.loc_id == data.loc_id)
        .with_for_update()
    )
    stock = (await db.execute(stmt)).scalar_one_or_none()
    if stock is None or stock.available <= 0:
        raise ValueError("Book not available at this location")

    stock.available -= 1
    stock.reserved  += 1

    booking = Booking(
        user_id=user_id,
        book_id=data.book_id,
        loc_id=data.loc_id,
        time_due=data.time_due or datetime.utcnow() + timedelta(days=14),
        stat="pending",
    )
    db.add(booking)
    await db.commit()

    stmt = select(Booking).options(*_FULL_LOAD).where(Booking.bk_id == booking.bk_id)
    full = (await db.execute(stmt)).scalar_one()
    return to_booking_out(full)


async def list_user_bookings(db: AsyncSession, user_id: int) -> list[BookingOut]:
    stmt = (
        select(Booking)
        .options(*_FULL_LOAD)
        .where(Booking.user_id == user_id)
        .order_by(Booking.time_created.desc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [to_booking_out(r) for r in rows]


async def close_booking(db: AsyncSession, bk_id: int) -> BookingOut:
    stmt = (
        select(Booking)
        .options(*_FULL_LOAD)
        .where(Booking.bk_id == bk_id)
        .with_for_update()
    )
    booking = (await db.execute(stmt)).scalar_one_or_none()
    if booking is None:
        raise ValueError("Booking not found")
    if booking.stat == "closed":
        raise ValueError("Booking already closed")

    stock = (await db.execute(
        select(Stock)
        .where(Stock.book_id == booking.book_id, Stock.loc_id == booking.loc_id)
        .with_for_update()
    )).scalar_one()

    stock.reserved  -= 1
    stock.available += 1
    booking.stat = "closed"
    booking.time_closed = datetime.utcnow()

    await db.commit()
    return to_booking_out(booking)