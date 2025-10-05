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
    # parents: List["Parent"] = Relationship(back_populates="student")
    # classes: List["StudentsClass"] = Relationship(back_populates="student")

    # quiz_responses: List["QuizResponse"] = Relationship(back_populates="student")
    # rewards_history: List["RewardHistory"] = Relationship(back_populates="student")
    # subject_activity_scores: List["SubjectActivityScore"] = Relationship(back_populates="student")
    # intolerances: List["FoodIntolerance"] = Relationship(link_model=StudentIntolerance)
    # allergies: List["AllergyInfo"] = Relationship(link_model=StudentAllergy)
    # medical: List["MedicalInfo"] = Relationship(link_model=StudentMedicalInfo)
