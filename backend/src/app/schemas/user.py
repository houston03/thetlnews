from pydantic import BaseModel
from datetime import datetime

class UserProfileResponse(BaseModel):
    email: str
    nickname: str
    created_at: datetime
    is_admin: bool

    class Config:
        orm_mode = True