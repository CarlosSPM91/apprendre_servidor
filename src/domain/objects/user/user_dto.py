
from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    username: str
    name: str
    last_name: str
    role: str