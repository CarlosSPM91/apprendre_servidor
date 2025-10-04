"""
Users DTO Object.


:author: Carlos S. Paredes Morillo
"""

from typing import Optional
from pydantic import BaseModel


class RoleDTO(BaseModel):
    role_id: int
    role_name: str