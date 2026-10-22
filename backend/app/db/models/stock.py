from sqlalchemy import ForeignKey, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (
        PrimaryKeyConstraint("book_id", "loc_id", name="stock_id"),
        CheckConstraint("available >= 0", name="stock_available_nonneg"),
        CheckConstraint("reserved  >= 0", name="stock_reserved_nonneg"),
    )

    book_id:   Mapped[int] = mapped_column(ForeignKey("books.book_id"))
    loc_id:    Mapped[int] = mapped_column(ForeignKey("locations.loc_id"))
    available: Mapped[int | None] = mapped_column(default=0)
    reserved:  Mapped[int | None] = mapped_column(default=0)

    book:     Mapped["Book"]     = relationship(back_populates="stock")
    location: Mapped["Location"] = relationship(back_populates="stock")
    