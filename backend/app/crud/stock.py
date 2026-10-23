from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Stock

async def get(db: AsyncSession, book_id: int, loc_id: int) -> Stock | None:
    return await db.scalar(
        select(Stock).where(
            Stock.book_id == book_id,
            Stock.loc_id == loc_id,
        )
    )

async def list_stock(db: AsyncSession) -> list[Stock]:
    result = await db.execute(
        select(Stock).order_by(Stock.book_id, Stock.loc_id)
    )
    return list(result.scalars().all())

async def create(db: AsyncSession, data: dict) -> Stock:
    stock = Stock(**data)
    db.add(stock)
    await db.commit()
    await db.refresh(stock)
    return stock

async def update(
    db: AsyncSession, book_id: int, loc_id: int, data: dict
) -> Stock | None:
    stock = await get(db, book_id, loc_id)
    if stock is None:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(stock, key, value)

    await db.commit()
    await db.refresh(stock)
    return stock

async def delete(db: AsyncSession, book_id: int, loc_id: int) -> bool:
    stock = await get(db, book_id, loc_id)
    if stock is None:
        return False
    await db.delete(stock)
    await db.commit()
    return True
