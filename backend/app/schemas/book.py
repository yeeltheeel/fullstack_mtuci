from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    descr: str | None = None

class StockItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    available: int | None
    reserved: int | None
    location: "LocationOut"

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    title: str | None
    author: str | None
   