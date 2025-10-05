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

from src.infrastructure.entities.course.activity_type import ActivityType
from src.infrastructure.entities.course.class_common_activity import ClassCommonActivity
from src.infrastructure.entities.course.course import Course
from src.infrastructure.entities.course.student_class import StudentClass

class CalendarActivity(SQLModel, table=True):
    __tablename__ = "calendar_activities"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    date: datetime
    activity_name: str = Field(max_length=50)
    activity_type_id: Optional[int] = Field(default=None, foreign_key="activity_type.id")

    # course: Course = Relationship(back_populates="calendar_activities")
    # activity_type: Optional[ActivityType] = Relationship(back_populates="calendar_activities")
    # students_classes: List[StudentClass] = Relationship(back_populates="common_activities", link_model=ClassCommonActivity)


