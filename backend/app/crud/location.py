from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Location
from app.schemas.location import LocationCreate, LocationOut


async def list_locations_out(db: AsyncSession) -> list[LocationOut]:
    rows = (await db.execute(select(Location).order_by(Location.loc_id))).scalars().all()
    return [LocationOut.model_validate(r) for r in rows]


async def create_location(db: AsyncSession, data: LocationCreate) -> LocationOut:
    loc = Location(
        country=data.country,
        city=data.city,
        street=data.street,
        house=data.house,
        descr=data.description,
    )
    db.add(loc)
    await db.commit()
    await db.refresh(loc)
    return LocationOut.model_validate(loc)