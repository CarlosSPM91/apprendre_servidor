"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field



class Role(SQLModel, table=True):
    """Database model for user roles.

    Attributes:
        id (Optional[int]): Primary key, role identifier.
        rol (str): Role name (unique, max length 64).
        users (List[User]): List of users assigned to this role.

    :author: Carlos S. Paredes Morillo
    """
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(max_length=64, nullable=False, sa_column_kwargs={"unique": True})

