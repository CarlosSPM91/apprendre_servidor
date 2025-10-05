"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.users.user import User

class Parent(SQLModel, table=True):
    __tablename__ = "parents"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    student_id: int = Field(foreign_key="students.id", index=True)

    user: User = Relationship()
