"""
Users DTO Object.

Data Transfer Object for user creation. Defines the fields required
to register or persist a new user.

:author: Carlos S. Paredes Morillo
"""

from pydantic import BaseModel


class UserCreateDTO(BaseModel):

    username: str
    email: str
    name: str
    last_name: str
    dni:str
    password: str
    phone: int
    role_id: int
