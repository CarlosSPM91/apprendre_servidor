"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.course.activity_type import ActivityType
from src.infrastructure.entities.course.subject_class import SubjectClass

class SubjectActivity(SQLModel, table=True):
    __tablename__ = "subject_activities"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject_class_id: int = Field(foreign_key="subject_class.id", index=True)
    subject_id: Optional[int] = Field(default=None, foreign_key="school_subjects.id")
    create_time: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))
    name: str = Field(max_length=50)
    activity_type_id: Optional[int] = Field(default=None, foreign_key="activity_type.id")

    # subject_class: SubjectClass = Relationship(back_populates="subject_activities")
    # activity_type: Optional[ActivityType] = Relationship(back_populates="subject_activities")
    # scores: List["SubjectActivityScore"] = Relationship(back_populates="subject_activity")



