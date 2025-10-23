"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class SubjectClass(SQLModel, table=True):
    __tablename__ = "subject_class"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    subject_id: int = Field(foreign_key="school_subjects.id", index=True) 
    class_id: Optional[int] = Field(default=None, foreign_key="classes.id")
    professor_id: Optional[int] = Field(default=None, foreign_key="teachers.id")
