
from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"
    user_id:str
    username:str
    role: int
