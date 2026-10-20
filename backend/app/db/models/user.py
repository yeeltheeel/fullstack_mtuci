from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class User(Base):
	__tablename__ = "users"

	user_id:  Mapped[int]  = mapped_column(primary_key=True)
	username:        Mapped[str]  = mapped_column(String(100), unique=True, index=True)
	hashed_password: Mapped[str]  = mapped_column(String(255))
	is_active:       Mapped[bool] = mapped_column(default=True)
