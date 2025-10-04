"""
Users DTO Object.


:author: Carlos S. Paredes Morillo
"""

from typing import Optional
from pydantic import BaseModel


class ChangePasswordDTO(BaseModel):
    user_id: int
    old_password: Optional[str] = None
    password: str