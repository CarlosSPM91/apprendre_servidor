"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class Reward(SQLModel, table=True):
    __tablename__ = "rewards"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    points: Optional[int] = None
