from enum import StrEnum

class BookingStatus(StrEnum):
	PENDING   = "pending"
	ONGOING   = "ongoing"
	LATE      = "late"
	CLOSED    = "closed"
	CANCELLED = "cancelled"
