from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import book as book_crud
from app.db.models import User
from app.schemas.book import BookFull
from app.schemas.location import LocationOut
from app.schemas.book import BookOut, BookCreate, BookUpdate, BookFull

router = APIRouter(prefix="/books", tags=["books"])

def _to_book_full(book, stock: dict) -> BookFull:
    return BookFull(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        genre=book.genre,
        descr=book.descr,
        available=stock.get("available", []),
        locations=[LocationOut.model_validate(l) for l in stock.get("locations", [])],
    )

@router.get("", response_model=list[BookFull])
async def list_books(db: AsyncSession = Depends(get_db)):
	# return await book_crud.list_books(db)
	books = await book_crud.list_books(db)
	stock = await book_crud.stock_by_book_ids(db, [b.book_id for b in books])
	return [_to_book_full(b, stock.get(b.book_id, {})) for b in books]

@router.get("/{book_id}", response_model=BookFull)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
	# book = await book_crud.get_by_id(db, book_id)
	# if book is None:
	#	raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found")
	# return book
	book = await book_crud.get_by_id(db, book_id)
	if book is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found")
	stock = await book_crud.stock_by_book_ids(db, [book.book_id])
	return _to_book_full(book, stock.get(book.book_id, {}))

@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(
	payload: BookCreate,
	db: AsyncSession = Depends(get_db),
	_: User = Depends(get_current_user),
):
	return await book_crud.create(db, payload.model_dump(exclude_unset=True))

@router.patch("/{book_id}", response_model=BookOut)
async def update_book(
	book_id: int,
	payload: BookUpdate,
	db: AsyncSession = Depends(get_db),
	_: User = Depends(get_current_user),
):
	book = await book_crud.update(db, book_id, payload.model_dump(exclude_unset=True))
	if book is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found")
	return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
	book_id: int,
	db: AsyncSession = Depends(get_db),
	_: User = Depends(get_current_user),
):
	ok = await book_crud.delete(db, book_id)
	if not ok:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found")
	