from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book, Stock
from app.schemas.book import BookCreate, BookOut
from app.schemas.location import LocationOut


def to_book_out(book: Book) -> BookOut:
    return BookOut(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        genre=book.genre,
        descr=book.descr,
        available=[s.loc_id for s in book.stock if s.available > 0],
        locations=[LocationOut.model_validate(s.location) for s in book.stock],
    )


async def list_books_out(db: AsyncSession) -> list[BookOut]:
    stmt = (
        select(Book)
        .options(selectinload(Book.stock).selectinload(Stock.location))
        .order_by(Book.book_id)
    )
    books = (await db.execute(stmt)).scalars().all()
    return [to_book_out(b) for b in books]


async def get_book_out(db: AsyncSession, book_id: int) -> BookOut | None:
    stmt = (
        select(Book)
        .options(selectinload(Book.stock).selectinload(Stock.location))
        .where(Book.book_id == book_id)
    )
    book = (await db.execute(stmt)).scalar_one_or_none()
    return to_book_out(book) if book else None


async def create_book(db: AsyncSession, data: BookCreate) -> BookOut:
    book = Book(
        title=data.title,
        author=data.author,
        genre=data.genre,
        descr=data.description,
    )
    db.add(book)
    await db.commit()
    db.expunge(book)
    loaded = await get_book_out(db, book.book_id)
    return loaded