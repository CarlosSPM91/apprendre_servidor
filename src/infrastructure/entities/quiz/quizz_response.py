"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.quiz.quiz import Quiz
from src.infrastructure.entities.student_info.student import Student

class QuizResponse(SQLModel, table=True):
    __tablename__ = "quiz_responses"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", index=True)
    response: Optional[str] = Field(default=None, max_length=250)
