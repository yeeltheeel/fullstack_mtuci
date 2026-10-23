from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import booking as booking_crud
from app.db.models import User
from app.schemas.booking import BookingOut, BookingCreate, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("", response_model=list[BookingOut])
async def list_all_bookings(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await booking_crud.list_bookings(db)

@router.get("/mine", response_model=list[BookingOut])
async def list_my_bookings(
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    return await booking_crud.list_bookings(db, user_id=current.user_id)

@router.get("/{bk_id}", response_model=BookingOut)
async def get_booking(
    bk_id: int,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    booking = await booking_crud.get_by_id(db, bk_id)
    if booking is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "booking not found")
    if booking.user_id != current.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "not your booking")
    return booking

@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    try:
        return await booking_crud.create(
            db,
            user_id=current.user_id,
            book_id=payload.book_id,
            loc_id=payload.loc_id,
            due_days=payload.due_days,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc))

@router.patch("/{bk_id}", response_model=BookingOut)
async def update_booking(
    bk_id: int,
    payload: BookingUpdate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    existing = await booking_crud.get_by_id(db, bk_id)
    if existing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "booking not found")
    if existing.user_id != current.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "not your booking")

    data = payload.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        data["status"] = data["status"].value if hasattr(data["status"], "value") else data["status"]

    try:
        booking = await booking_crud.update(db, bk_id, data)
    except ValueError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc))

    if booking is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "booking not found")
    return booking

@router.delete("/{bk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    bk_id: int,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    existing = await booking_crud.get_by_id(db, bk_id)
    if existing is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "booking not found")
    if existing.user_id != current.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "not your booking")
    await booking_crud.delete(db, bk_id)
    