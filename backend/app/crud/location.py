from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Location

async def get_by_id(db: AsyncSession, loc_id: int) -> Location | None:
    return await db.get(Location, loc_id)

async def list_locations(db: AsyncSession) -> list[Location]:
    result = await db.execute(select(Location).order_by(Location.loc_id))
    return list(result.scalars().all())

async def create(db: AsyncSession, data: dict) -> Location:
    location = Location(**data)
    db.add(location)
    await db.commit()
    await db.refresh(location)
    return location

async def update(db: AsyncSession, loc_id: int, data: dict) -> Location | None:
    location = await db.get(Location, loc_id)
    if location is None:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(location, key, value)

    await db.commit()
    await db.refresh(location)
    return location

async def delete(db: AsyncSession, loc_id: int) -> bool:
    location = await db.get(Location, loc_id)
    if location is None:
        return False
    await db.delete(location)
    await db.commit()
    return True
