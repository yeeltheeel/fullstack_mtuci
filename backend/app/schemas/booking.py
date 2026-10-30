from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserOut
from app.schemas.book import BookBrief
from app.schemas.location import LocationOut

class BookingStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    OVERDUE = "overdue"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class BookingCreate(BaseModel):
    book_id: int
    loc_id: int
    due_days: int = Field(default=14, ge=1, le=90)

class BookingUpdate(BaseModel):
    status: BookingStatus | None = None
    time_due: datetime | None = None

class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bk_id: int
    user: UserOut
    book: BookBrief
    location: LocationOut
    time_created: datetime
    time_due: datetime | None
    time_closed: datetime | None
    stat: BookingStatus
    