from pydantic import BaseModel, Field, AliasChoices

class LocationOut(BaseModel):
    id: int = Field(validation_alias=AliasChoices("loc_id", "id"))
    country: str
    city: str
    street: str
    house: str
    description: str = Field(validation_alias=AliasChoices("descr", "description"))

    model_config = {"from_attributes": True, "populate_by_name": True}


class LocationCreate(BaseModel):
    country: str
    city: str
    street: str
    house: str
    description: str