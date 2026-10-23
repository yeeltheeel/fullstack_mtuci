from pydantic import BaseModel, ConfigDict

class LocationOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	loc_id: int
	country: str | None
	city: str | None
	street: str | None
	house: str | None
	descr: str | None

class LocationCreate(BaseModel):
	country: str | None = None
	city: str | None = None
	street: str | None = None
	house: str | None = None
	descr: str | None = None

class LocationUpdate(BaseModel):
	country: str | None = None
	city: str | None = None
	street: str | None = None
	house: str | None = None
	descr: str | None = None
