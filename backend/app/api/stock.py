from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import stock as stock_crud
from app.db.models import User
from app.schemas.stock import StockOut, StockCreate, StockUpdate

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("", response_model=list[StockOut])
async def list_stock(db: AsyncSession = Depends(get_db)):
    return await stock_crud.list_stock(db)

@router.get("/{book_id}/{loc_id}", response_model=StockOut)
async def get_stock(
    book_id: int,
    loc_id: int,
    db: AsyncSession = Depends(get_db),
):
    stock = await stock_crud.get(db, book_id, loc_id)
    if stock is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "stock not found")
    return stock

@router.post("", response_model=StockOut, status_code=status.HTTP_201_CREATED)
async def create_stock(
    payload: StockCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        return await stock_crud.create(db, payload.model_dump())
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "stock already exists for this book/location",
        )

@router.patch("/{book_id}/{loc_id}", response_model=StockOut)
async def update_stock(
    book_id: int,
    loc_id: int,
    payload: StockUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stock = await stock_crud.update(
        db, book_id, loc_id, payload.model_dump(exclude_unset=True)
    )
    if stock is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "stock not found")
    return stock

@router.delete("/{book_id}/{loc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(
    book_id: int,
    loc_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ok = await stock_crud.delete(db, book_id, loc_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "stock not found")
    