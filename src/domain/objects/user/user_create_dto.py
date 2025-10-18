"""
Users DTO Object.

Data Transfer Object for user creation. Defines the fields required
to register or persist a new user.

:author: Carlos S. Paredes Morillo
"""

from typing import Optional
from pydantic import BaseModel


class UserCreateDTO(BaseModel):

    username: str
    email: Optional[str] = None
    name: str
    last_name: str
    dni:Optional[str] = None
    password: str
    phone: Optional[int] = None
    role_id: int
