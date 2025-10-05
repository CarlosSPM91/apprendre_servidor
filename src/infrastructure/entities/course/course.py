"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    year: Optional[int] = None
    password: Optional[str] = Field(default=None, max_length=50)
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
