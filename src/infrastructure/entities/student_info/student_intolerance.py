"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from sqlmodel import Relationship, SQLModel, Field

class StudentIntolerance(SQLModel, table=True):
    __tablename__ = "students_intolerances"

    students_user_id: int = Field(foreign_key="students.id", primary_key=True)
    food_intolerance_id: int = Field(foreign_key="food_intolerances.id", primary_key=True)




