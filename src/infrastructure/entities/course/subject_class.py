"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.course.course import Course
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.entities.users.professor import Professor

class SubjectClass(SQLModel, table=True):
    __tablename__ = "subject_class"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    subject_id: int = Field(foreign_key="school_subjects.id", index=True) 
    students_class_id: Optional[int] = Field(default=None, foreign_key="student_class.id")
    professor_id: Optional[int] = Field(default=None, foreign_key="professors.id")

    # course: Course = Relationship(back_populates="subject_classes")
    # subject: SchoolSubject = Relationship(back_populates="subject_classes")
    # students_class: Optional[StudentClass] = Relationship(back_populates="subject_classes")
    # professor: Optional[Professor] = Relationship(back_populates="subject_classes")

    # subject_activities: List["SubjectActivity"] = Relationship(back_populates="subject_class")
    # quizzes: List["Quiz"] = Relationship(back_populates="subject_class")



