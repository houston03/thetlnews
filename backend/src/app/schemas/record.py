from pydantic import BaseModel, Field
from typing import Optional

class RecordBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    example: Optional[str]
    extended_description: Optional[str]

class RecordCreate(RecordBase):
    pass

class RecordUpdate(RecordBase):
    pass

class RecordResponse(RecordBase):
    id: int

    class Config:
        orm_mode = True
