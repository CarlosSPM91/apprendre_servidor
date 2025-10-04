"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.student_info.student_medical_info import StudentMedicalInfo

if TYPE_CHECKING:
    from src.infrastructure.entities.student_info.student import Student

class MedicalInfo(SQLModel, table=True):
    __tablename__ = "medical_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=100)
    medication: Optional[str] = Field(default=None, max_length=100)

    students: List[Student] = Relationship(back_populates="medical", link_model=StudentMedicalInfo)

