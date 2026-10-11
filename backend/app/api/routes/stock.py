from fastapi import APIRouter
from app.api.depends import DB, CurrentUser
from app.crud import stock as crud
from app.schemas.stock import StockCreate, StockOut

router = APIRouter(prefix="/api/stock", tags=["stock"])


@router.get("/", response_model=list[StockOut])
async def list_stock(db: DB):
    return await crud.list_stock(db)


@router.post("/", response_model=StockOut, status_code=201)
async def upsert_stock(payload: StockCreate, db: DB, _: CurrentUser):
    return await crud.upsert_stock(db, payload)