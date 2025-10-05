"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class Quiz(SQLModel, table=True):
    __tablename__ = "quiz"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: Optional[int] = Field(default=None, foreign_key="school_subjects.id", index=True)
    question: str = Field(max_length=100)
    solution: Optional[int] = None
    points: Optional[int] = None
