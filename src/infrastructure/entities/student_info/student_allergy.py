"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from sqlmodel import SQLModel, Field

class StudentAllergy(SQLModel, table=True):
    __tablename__ = "students_allergies"

    students_user_id: int = Field(foreign_key="students.id", primary_key=True)
    allergies_info_id: int = Field(foreign_key="allergies_info.id", primary_key=True)




