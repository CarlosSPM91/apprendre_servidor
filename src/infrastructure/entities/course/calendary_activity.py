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



class CalendarActivity(SQLModel, table=True):
    __tablename__ = "calendar_activities"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    date: datetime
    activity_name: str = Field(max_length=50)
    activity_type_id: Optional[int] = Field(default=None, foreign_key="activity_type.id")
