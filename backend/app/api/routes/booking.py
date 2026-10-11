from fastapi import APIRouter, HTTPException
from app.api.depends import DB, CurrentUser
from app.crud import booking as crud
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("/", response_model=BookingOut, status_code=201)
async def create(data: BookingCreate, db: DB, current: CurrentUser):
    try:
        return await crud.create_booking(db, current.user_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/me", response_model=list[BookingOut])
async def mine(db: DB, current: CurrentUser):
    return await crud.list_user_bookings(db, current.user_id)


@router.patch("/{bk_id}/close", response_model=BookingOut)
async def close(bk_id: int, db: DB, _: CurrentUser):
    try:
        return await crud.close_booking(db, bk_id)
    except ValueError as e:
        raise HTTPException(400, str(e))