from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
	__tablename__ = "users"

	user_id:       Mapped[int]  = mapped_column(primary_key=True)
	username:      Mapped[str | None] = mapped_column(String(255))
	birthday:      Mapped[date | None] = mapped_column(Date)
	email:         Mapped[str]  = mapped_column(String(255), unique=True)
	avatar_url:    Mapped[str | None] = mapped_column(String(255))
	password_hash: Mapped[str]  = mapped_column("pass", String(255))

	bookings: Mapped[list["Booking"]] = relationship(back_populates="user")
