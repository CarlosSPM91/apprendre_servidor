"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Column, ForeignKey, Integer, Relationship, SQLModel, Field

from src.infrastructure.entities.student_info.student_allergy import StudentAllergy
from src.infrastructure.entities.student_info.student_intolerance import StudentIntolerance
from src.infrastructure.entities.student_info.student_medical_info import StudentMedicalInfo
from src.infrastructure.entities.users.user import User

class Student(SQLModel, table=True):
    __tablename__ = "students"

    id: Optional[int] = Field(default=None, primary_key=True)
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    medical_id: Optional[int] = Field(default=None) 
    allergies_id: Optional[int] = Field(default=None)  
    food_intolerance_id: Optional[int] = Field(default=None) 
    observations: Optional[str] = Field(default=None, max_length=500)

    user: User = Relationship()

