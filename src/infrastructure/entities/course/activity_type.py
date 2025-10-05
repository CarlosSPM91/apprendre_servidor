"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class ActivityType(SQLModel, table=True):
    __tablename__ = "activity_type"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(max_length=20, nullable=False, sa_column_kwargs={"unique": True})

    # calendar_activities: List["CalendarActivity"] = Relationship(back_populates="activity_type")
    # subject_activities: List["SubjectActivity"] = Relationship(back_populates="activity_type")
