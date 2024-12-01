from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    gold: int
    diamond: int
    status: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    gold: int
    diamond: int 