from pydantic import BaseModel, Field, AliasChoices
from app.schemas.location import LocationOut

class BookOut(BaseModel):
    id: int = Field(validation_alias=AliasChoices("book_id", "id"))
    title: str
    author: str
    genre: str
    description: str = Field(validation_alias=AliasChoices("descr", "description"))
    available: list[int] = []
    locations: list[LocationOut] = []

    model_config = {"from_attributes": True, "populate_by_name": True}


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    description: str