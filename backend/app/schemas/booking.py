from datetime import datetime
from pydantic import BaseModel, Field, AliasChoices
from app.schemas.user import UserOut
from app.schemas.book import BookOut
from app.schemas.location import LocationOut

class BookingOut(BaseModel):
    id: int = Field(validation_alias=AliasChoices("bk_id", "id"))
    user: UserOut
    book: BookOut
    location: LocationOut
    time_created: datetime
    time_due: datetime | None = None
    time_closed: datetime | None = None
    status: str = Field(validation_alias=AliasChoices("stat", "status"))

    model_config = {"from_attributes": True, "populate_by_name": True}


class BookingCreate(BaseModel):
    book_id: int
    loc_id: int
    time_due: datetime | None = None