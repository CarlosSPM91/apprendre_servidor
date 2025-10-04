"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.quiz.quiz import Quiz
from src.infrastructure.entities.student_info.student import Student

class QuizResponse(SQLModel, table=True):
    __tablename__ = "quiz_responses"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id", index=True)
    student_id: int = Field(foreign_key="students.id", index=True)
    response: Optional[str] = Field(default=None, max_length=250)

    quiz: Quiz = Relationship(back_populates="responses")
    student: Student = Relationship(back_populates="quiz_responses")


