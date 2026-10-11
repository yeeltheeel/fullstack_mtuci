from fastapi import APIRouter
from app.api.depends import DB, CurrentUser
from app.crud import location as crud
from app.schemas.location import LocationCreate, LocationOut

router = APIRouter(prefix="/api/locations", tags=["locations"])


@router.get("/", response_model=list[LocationOut])
async def list_locations(db: DB):
    return await crud.list_locations_out(db)


@router.post("/", response_model=LocationOut, status_code=201)
async def create_location(payload: LocationCreate, db: DB, _: CurrentUser):
    return await crud.create_location(db, payload)