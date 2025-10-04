"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from sqlmodel import SQLModel, Field

class StudentMedicalInfo(SQLModel, table=True):
    __tablename__ = "students_medical_info"

    students_user_id: int = Field(foreign_key="students.id", primary_key=True)
    medical_info_id: int = Field(foreign_key="medical_info.id", primary_key=True)




