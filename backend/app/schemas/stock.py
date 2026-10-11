from pydantic import BaseModel, Field

class StockCreate(BaseModel):
    book_id: int
    loc_id:  int
    available: int = Field(0, ge=0)

class StockOut(BaseModel):
    book_id: int
    loc_id:  int
    available: int
    reserved: int
    model_config = {"from_attributes": True}