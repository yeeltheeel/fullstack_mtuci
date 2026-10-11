from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Stock
from app.schemas.stock import StockCreate, StockOut


async def list_stock(db: AsyncSession) -> list[StockOut]:
    rows = (await db.execute(select(Stock))).scalars().all()
    return [StockOut.model_validate(r) for r in rows]


async def upsert_stock(db: AsyncSession, data: StockCreate) -> StockOut:
    stock = await db.get(Stock, (data.book_id, data.loc_id))
    if stock is None:
        stock = Stock(book_id=data.book_id, loc_id=data.loc_id,
                      available=data.available, reserved=0)
        db.add(stock)
    else:
        stock.available = data.available
    await db.commit()
    await db.refresh(stock)
    return StockOut.model_validate(stock)