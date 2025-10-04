"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.course.subject_activity import SubjectActivity
from src.infrastructure.entities.student_info.student import Student

class SubjectActivityScore(SQLModel, table=True):
    __tablename__ = "subject_activities_copy"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject_activity_id: int = Field(foreign_key="subject_activities.id", index=True)
    student_id: int = Field(foreign_key="students.id", index=True)
    note: Optional[float] = None

    subject_activity: SubjectActivity = Relationship(back_populates="scores")
    student: Student = Relationship(back_populates="subject_activity_scores")


