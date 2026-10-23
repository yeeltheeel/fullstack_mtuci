from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import book as book_crud
from app.db.models import User
from app.schemas.book import BookOut, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=list[BookOut])
async def list_books(db: AsyncSession = Depends(get_db)):
    return await book_crud.list_books(db)

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_crud.get_by_id(db, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found")
    return book

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
    