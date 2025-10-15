"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class Classes(SQLModel, table=True):
    __tablename__ = "classes"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id")
    student_class_id: int = Field(foreign_key="student_class.id")
    tutor_id: Optional[int] = Field(default=None, foreign_key="professors.id")
