from datetime import datetime
from sqlalchemy import ForeignKey, ForeignKeyConstraint, CheckConstraint, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Booking(Base):
	__tablename__ = "bookings"
	__table_args__ = (
		ForeignKeyConstraint(
			["book_id", "loc_id"],
			["stock.book_id", "stock.loc_id"],
			name="stock_id",
		),
		CheckConstraint(
			"stat in ('pending', 'ongoing', 'late', 'closed', 'cancelled')",
			name="ck_booking_stat",
		),
	)

	bk_id:        Mapped[int] = mapped_column(primary_key=True)
	user_id:      Mapped[int | None] = mapped_column(ForeignKey("users.user_id"))
	book_id:      Mapped[int | None]
	loc_id:       Mapped[int | None]
	time_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
	time_due:     Mapped[datetime | None] = mapped_column(DateTime)
	time_closed:  Mapped[datetime | None] = mapped_column(DateTime)
	stat:         Mapped[str] = mapped_column(String(255), default="pending")

	user:     Mapped["User"]     = relationship(back_populates="bookings")
	book:     Mapped["Book"]     = relationship(back_populates="bookings")
	location: Mapped["Location"] = relationship(back_populates="bookings")
	