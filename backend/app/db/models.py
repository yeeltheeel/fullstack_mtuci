from datetime import date, datetime
from sqlalchemy import (
    Integer, String, Date, DateTime, ForeignKey,
    CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    user_id:  Mapped[int]         = mapped_column(Integer, primary_key=True)
    username: Mapped[str]         = mapped_column(String(100), nullable=False)
    birthday: Mapped[date | None] = mapped_column(Date)
    email:    Mapped[str]         = mapped_column(String(100), unique=True, nullable=False)
    avatar:   Mapped[str | None]  = mapped_column(String(100))
    pass_:    Mapped[str]         = mapped_column("pass", String(100), nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int]        = mapped_column(Integer, primary_key=True)
    title:   Mapped[str]        = mapped_column(String(100), nullable=False)
    author:  Mapped[str]        = mapped_column(String(100), nullable=False)
    genre:   Mapped[str]        = mapped_column(String(100), nullable=False)
    descr:   Mapped[str]        = mapped_column(String(300), nullable=False)

    stock: Mapped[list["Stock"]] = relationship(back_populates="book")


class Location(Base):
    __tablename__ = "locations"
    loc_id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    city:    Mapped[str] = mapped_column(String(100), nullable=False)
    street:  Mapped[str] = mapped_column(String(100), nullable=False)
    house:   Mapped[str] = mapped_column(String(100), nullable=False)
    descr:   Mapped[str] = mapped_column(String(300), nullable=False)

    stock: Mapped[list["Stock"]] = relationship(back_populates="location")


class Stock(Base):
    __tablename__ = "stock"
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), nullable=False)
    loc_id:  Mapped[int] = mapped_column(ForeignKey("locations.loc_id"), nullable=False)
    available: Mapped[int] = mapped_column(Integer, default=0)
    reserved:  Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        PrimaryKeyConstraint("book_id", "loc_id", name="stock_pkey"),
        CheckConstraint("available >= 0", name="stock_available_chk"),
        CheckConstraint("reserved >= 0",  name="stock_reserved_chk"),
    )

    book:     Mapped["Book"]     = relationship(back_populates="stock")
    location: Mapped["Location"] = relationship(back_populates="stock")


class Booking(Base):
    __tablename__ = "bookings"
    bk_id:        Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:      Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    book_id:      Mapped[int] = mapped_column(Integer, nullable=False)
    loc_id:       Mapped[int] = mapped_column(ForeignKey("locations.loc_id"), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    time_due:     Mapped[datetime | None] = mapped_column(DateTime)
    time_closed:  Mapped[datetime | None] = mapped_column(DateTime)
    stat:         Mapped[str] = mapped_column(String(100), nullable=False, default="pending")

    __table_args__ = (
        ForeignKeyConstraint(
            ["book_id", "loc_id"],
            ["stock.book_id", "stock.loc_id"],
            name="booking_stock_fk",
        ),
    )

    user:     Mapped["User"]     = relationship(back_populates="bookings")
    book:     Mapped["Book"]     = relationship()
    location: Mapped["Location"] = relationship()