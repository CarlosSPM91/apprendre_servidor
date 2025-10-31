"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.student_info.student_allergy import StudentAllergy

class AllergyInfo(SQLModel, table=True):
    __tablename__ = "allergies_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    name:str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=250)


