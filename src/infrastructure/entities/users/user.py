"""
Users Entity.

Represents the `users` table in the database with its fields,
relationships, and constraints.

:author: Carlos S. Paredes Morillo
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        sa_column_kwargs={"unique": True}, max_length=30, nullable=False
    )
    name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=100)
    email: str = Field(default=None, max_length=100, nullable=True, unique=True)
    phone: int = Field(default=None, nullable=True)
    dni: Optional[str] = Field(default=None, max_length=10, nullable=True)
    password: str = Field(nullable=False, max_length=255)
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_used: Optional[datetime] = Field(default=None)
    role_id: int = Field(default=None, foreign_key="roles.id")

