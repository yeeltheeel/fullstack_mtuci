from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Location(Base):
    __tablename__ = "locations"

    loc_id:  Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str | None] = mapped_column(String(255))
    city:    Mapped[str | None] = mapped_column(String(255))
    street:  Mapped[str | None] = mapped_column(String(255))
    house:   Mapped[str | None] = mapped_column(String(255))
    descr:   Mapped[str | None] = mapped_column(String(255))

    stock:    Mapped[list["Stock"]]   = relationship(back_populates="location")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="location")
    