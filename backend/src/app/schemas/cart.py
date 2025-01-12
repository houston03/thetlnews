from pydantic import BaseModel

class CartBase(BaseModel):
    record_id: int

class CartAdd(CartBase):
    pass

class CartResponse(CartBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
