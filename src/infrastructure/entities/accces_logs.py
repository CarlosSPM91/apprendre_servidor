"""
Access Logs Entity.

Represents the `access_log` table in the database, used to store
user access information.

:author: Carlos S. Paredes Morillo
"""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel

from src.infrastructure.entities.user import User


class AccesLog(SQLModel, table=True):
    """Database model for user access logs.

    Attributes:
        id (Optional[int]): Primary key, access log identifier.
        user_id (int): Foreign key referencing `users.id`.
        email (str): Email address used during the access.
        acces_date (datetime): Timestamp of the access event.
        users (User): Relationship to the user entity.

    :author: Carlos S. Paredes Morillo
    """
    __tablename__ = "access_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    email: str = Field(default=None, nullable=False, max_length=255)
    acces_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    users: "User" = Relationship(
        back_populates="access_log",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
