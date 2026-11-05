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
	# insert as pending (audit trail)
	booking = Booking(
		user_id=user_id,
		book_id=book_id,
		loc_id=loc_id,
		time_due=datetime.now(timezone.utc) + timedelta(days=due_days),
		stat="pending",
	)
	db.add(booking)
	await db.flush() # get bk_id, but don't commit yet

	# run validations
	reasons: list[str] = []
	stock = await db.scalar(
		select(Stock)
		.where(Stock.book_id == book_id, Stock.loc_id == loc_id)
		.with_for_update()
	)
	if stock is None or (stock.available or 0) < 1:
		reasons.append("no available copies at this location")

	# duplicate check — same user, same book, same location, already active
	existing = await db.scalar(
		select(Booking.bk_id).where(
			Booking.user_id == user_id,
			Booking.book_id == book_id,
			Booking.loc_id == loc_id,
			Booking.stat.in_(("pending", "active", "overdue")),
			Booking.bk_id != booking.bk_id,
		)
	)
	if existing is not None:
		reasons.append("already booked by this user")

	# reject -> cancelled, return 409
	if reasons:
		booking.stat = "cancelled"
		await db.commit()
		raise ValueError("; ".join(reasons))

	# accept -> active, decrement stock
	stock.available -= 1
	stock.reserved += 1
	booking.stat = "active"
	await db.commit()
	await db.refresh(booking)

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

async def update_status(
	db: AsyncSession, bk_id: int, *, status: str,
) -> Booking | None:
	booking = await db.scalar(
		select(Booking).where(Booking.bk_id == bk_id).with_for_update()
	)
	if booking is None:
		return None

	old = booking.stat
	new = status

	if new == old:
		# idempotent — re-clicking "cancel" doesn't error
		return await get_by_id(db, bk_id)

	allowed = {
		"pending":   {"active", "cancelled"},
		"active":    {"closed", "overdue", "cancelled"},
		"overdue":   {"closed", "cancelled"},
		"closed":    set(), # terminal
		"cancelled": set(), # terminal
	}
	if new not in allowed.get(old, set()):
		raise ValueError(f"cannot transition {old} → {new}")

	# release reserved slot on transition out of an active state
	if old in ("pending", "active", "overdue") and new in ("closed", "cancelled"):
		stock = await db.scalar(
			select(Stock)
			.where(Stock.book_id == booking.book_id, Stock.loc_id == booking.loc_id)
			.with_for_update()
		)
		if stock:
			stock.reserved = max(0, (stock.reserved or 0) - 1)
			stock.available = (stock.available or 0) + 1

	booking.stat = new
	if new in ("closed", "cancelled"):
		booking.time_closed = datetime.now(timezone.utc)

	await db.commit()
	await db.refresh(booking)
	return await get_by_id(db, bk_id)

