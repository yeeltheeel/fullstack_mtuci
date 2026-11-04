from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book, Stock, Location

def _full(stmt):
	return stmt.options(
		selectinload(Book.stock).selectinload(Stock.location)
	)

async def get_by_id(db: AsyncSession, book_id: int) -> Book | None:
	return await db.scalar(
		_full(select(Book).where(Book.book_id == book_id))
	)

async def list_books(db: AsyncSession) -> list[Book]:
	result = await db.execute(
		_full(select(Book).order_by(Book.book_id))
	)
	return list(result.scalars().all())

async def create(db: AsyncSession, data: dict) -> Book:
	book = Book(**data)
	db.add(book)
	await db.commit()
	return await get_by_id(db, book.book_id)

async def update(db: AsyncSession, book_id: int, data: dict) -> Book | None:
	book = await db.get(Book, book_id)
	if book is None:
		return None

	for key, value in data.items():
		if value is not None:
			setattr(book, key, value)

	await db.commit()
	return await get_by_id(db, book_id)

async def delete(db: AsyncSession, book_id: int) -> bool:
	book = await db.get(Book, book_id)
	if book is None:
		return False
	await db.delete(book)
	await db.commit()
	return True

async def stock_by_book_ids(
	db: AsyncSession, book_ids: list[int],
) -> dict[int, dict]:
	"""{book_id: {"available": [loc_id...], "locations": [Location...]}}"""
	if not book_ids:
		return {}
	rows = (await db.execute(
		select(Stock.book_id, Stock.available, Location)
		.join(Location, Location.loc_id == Stock.loc_id)
		.where(Stock.book_id.in_(book_ids))
	)).all()

	out: dict[int, dict] = defaultdict(lambda: {"available": [], "locations": []})
	for book_id, available, loc in rows:
		if (available or 0) > 0:
			out[book_id]["available"].append(available)
			out[book_id]["locations"].append(loc)
	return out
