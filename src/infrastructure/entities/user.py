"""
Users Entity.

Represents the `users` table in the database with its fields,
relationships, and constraints.

:author: Carlos S. Paredes Morillo
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel

from src.infrastructure.entities.accces_logs import AccesLog
from src.infrastructure.entities.roles import Role


class User(SQLModel, table=True):
    """Database model for application users.

    Attributes:
        id (Optional[int]): Primary key, user identifier.
        username (str): Unique username.
        name (str): User's first name.
        last_names (str): User's last names.
        email (Optional[str]): User's email address.
        phone (int): User's phone number (9 digits max).
        dni (Optional[str]): National identification number (max length 10).
        password (str): User's hashed password.
        create_time (datetime): User creation timestamp.
        last_used (Optional[datetime]): Last login timestamp.
        role_id (int): Foreign key referencing `roles.id`.
        role (Role): Relationship to the associated role.
        access_logs (List[AccesLog]): Relationship to access logs.

    :author: Carlos S. Paredes Morillo
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        sa_column_kwargs={"unique": True}, max_length=255, nullable=False
    )
    name: str = Field(nullable=False, max_length=50)
    last_names: str = Field(nullable=False, max_length=100)
    email: str | None
    phone: int = Field(nullable=False, max_length=9)
    dni: Optional[str] = Field(default=None, max_length=10)
    password: str = Field(nullable=False, max_length=255)
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_used: Optional[datetime] = Field(default=None)
    role_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("roles.id", ondelete="RESTRICT"),
            nullable=False
        ),
        index=True
    )

    role: "Role" = Relationship(back_populates="users")
    access_logs: List["AccesLog"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
            "lazy": "selectin",
        },
    )
