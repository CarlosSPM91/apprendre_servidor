"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.course.class_common_activity import ClassCommonActivity
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.users.professor import Professor

class StudentClass(SQLModel, table=True):
    __tablename__ = "student_class"

    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="students.id", index=True)
    points: Optional[int] = 0
    tutor_id: Optional[int] = Field(default=None, foreign_key="professors.id")

    # student: Student = Relationship(back_populates="classes")
    # tutor: Optional[Professor] = Relationship(back_populates="tutor_of")
    # subject_classes: List["SubjectClass"] = Relationship(back_populates="students_class")
    # common_activities: List["CalendarActivity"] = Relationship(back_populates="students_classes", link_model=ClassCommonActivity)


