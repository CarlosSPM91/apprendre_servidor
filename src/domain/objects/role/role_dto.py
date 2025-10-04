"""
Users DTO Object.


:author: Carlos S. Paredes Morillo
"""

from pydantic import BaseModel


class RoleDTO(BaseModel):
    role_id: int
    role_name: str