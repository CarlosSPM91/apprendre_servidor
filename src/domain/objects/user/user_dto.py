
from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    name: str
    lastname: str
    token: str
    role: str