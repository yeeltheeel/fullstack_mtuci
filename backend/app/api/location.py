from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import location as location_crud
from app.db.models import User
from app.schemas.location import LocationOut, LocationCreate, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("", response_model=list[LocationOut])
async def list_locations(db: AsyncSession = Depends(get_db)):
    return await location_crud.list_locations(db)

@router.get("/{loc_id}", response_model=LocationOut)
async def get_location(loc_id: int, db: AsyncSession = Depends(get_db)):
    loc = await location_crud.get_by_id(db, loc_id)
    if loc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "location not found")
    return loc

@router.post("", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(
    payload: LocationCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await location_crud.create(db, payload.model_dump(exclude_unset=True))

@router.patch("/{loc_id}", response_model=LocationOut)
async def update_location(
    loc_id: int,
    payload: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    loc = await location_crud.update(db, loc_id, payload.model_dump(exclude_unset=True))
    if loc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "location not found")
    return loc

@router.delete("/{loc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    loc_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ok = await location_crud.delete(db, loc_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "location not found")
    