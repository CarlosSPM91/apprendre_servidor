"""
User Data Transfer Object (DTO).

Represents a user object for responses or data transfer between layers.
This object is used to return user information without sensitive fields 
like passwords.

Attributes:
    user_id (int): Unique identifier of the user.
    username (str): The username of the user.
    name (str): First name of the user.
    last_name (str): Last name of the user.
    role (int): Role ID assigned to the user.

:author: Carlos S. Paredes Morillo
"""

from typing import Optional
from pydantic import BaseModel

class UserDTO(BaseModel):
    user_id: int
    username: str
    name: str
    last_name: str
    phone: Optional[int] = None
    dni: Optional[str] = None
    role: int
