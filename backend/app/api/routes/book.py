from fastapi import APIRouter, HTTPException
from app.api.depends import DB, CurrentUser
from app.crud import book as crud
from app.schemas.book import BookCreate, BookOut

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("/", response_model=list[BookOut])
async def list_books(db: DB):
    return await crud.list_books_out(db)


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: DB):
    book = await crud.get_book_out(db, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    return book


@router.post("/", response_model=BookOut, status_code=201)
async def create_book(payload: BookCreate, db: DB, _: CurrentUser):
    return await crud.create_book(db, payload)