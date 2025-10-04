"""
Users DTO Object.


:author: Carlos S. Paredes Morillo
"""

from typing import Optional
from pydantic import BaseModel


class UserUpdateDTO(BaseModel):
    user_id: int
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    dni: Optional[str] = None
    role_id: Optional[int] = None