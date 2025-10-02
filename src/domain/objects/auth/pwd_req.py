
from pydantic import BaseModel


class PasswordRequest(BaseModel):
    user_id:int
    password: str
