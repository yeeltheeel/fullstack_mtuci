from pydantic import BaseModel, ConfigDict, Field

class StockOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    loc_id: int
    available: int | None
    reserved: int | None

class StockCreate(BaseModel):
    book_id: int
    loc_id: int
    available: int = Field(default=0, ge=0)
    reserved: int = Field(default=0, ge=0)

class StockUpdate(BaseModel):
    available: int | None = Field(default=None, ge=0)
    reserved: int | None = Field(default=None, ge=0)
    