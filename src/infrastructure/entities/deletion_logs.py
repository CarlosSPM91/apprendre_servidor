"""
Access Logs Entity.

Represents the `deletion_log` table in the database, used to store
user access information.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class DeletionLog(SQLModel, table=True):
    """Database model for user access logs.

    Attributes:
        id (Optional[int]): Primary key, access log identifier.
        user_id (int): Foreign key referencing `users.id`.
        email (str): Email address used during the access.
        acces_date (datetime): Timestamp of the access event.
        users (User): Relationship to the user entity.

    :author: Carlos S. Paredes Morillo
    """

    __tablename__ = "deletion_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    name: str = Field(default=None, nullable=False, max_length=50)
    last_name: str = Field(default=None, nullable=False, max_length=100)
    deletion_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user_who_deleted: int
    name_who_deleted: str = Field(default=None, nullable=False, max_length=50)
    last_name_who_deleted: str = Field(default=None, nullable=False, max_length=100)
