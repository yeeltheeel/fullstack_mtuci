from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title:   Mapped[str | None] = mapped_column(String(255))
    author:  Mapped[str | None] = mapped_column(String(255))
    genre:   Mapped[str | None] = mapped_column(String(255))
    descr:   Mapped[str | None] = mapped_column(String(300))

    stock:    Mapped[list["Stock"]]   = relationship(back_populates="book")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="book")
    