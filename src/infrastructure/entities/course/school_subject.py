"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class SchoolSubject(SQLModel, table=True):
    __tablename__ = "school_subjects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    description: Optional[str] = Field(default=None, max_length=100)
