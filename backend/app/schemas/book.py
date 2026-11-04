from pydantic import BaseModel, ConfigDict
from app.schemas import LocationOut

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
	title: str | None = None
	author: str | None = None
	genre: str | None = None
	descr: str | None = None

# class BookBrief(BaseModel):
# 	model_config = ConfigDict(from_attributes=True)
# 	book_id: int
# 	title: str | None
# 	author: str | None
# 	genre: str | None
# 	descr: str | None

class BookUpdate(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	book_id: int | None = None
	title: str | None = None
	author: str | None = None
	genre: str | None = None
	descr: str | None = None

class BookFull(BookOut):
    available: list[int]
    locations: list[LocationOut]
