"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from sqlmodel import SQLModel, Field

class ClassCommonActivity(SQLModel, table=True):
    __tablename__ = "class_common_activities"

    students_class_id: int = Field(foreign_key="student_class.id", primary_key=True)
    calendar_activities_id: int = Field(foreign_key="calendar_activities.id", primary_key=True)


