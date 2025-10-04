"""
Role Entity.

Represents the role table in the database. Each role can be
associated with multiple users.

:author: Carlos S. Paredes Morillo
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import  Optional
from sqlmodel import Relationship, SQLModel, Field

from src.infrastructure.entities.quiz.reward import Reward
from src.infrastructure.entities.student_info.student import Student

class RewardHistory(SQLModel, table=True):
    __tablename__ = "rewards_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    reward_id: int = Field(foreign_key="rewards.id", index=True)
    student_id: int = Field(foreign_key="students.id", index=True, ondelete="CASCADE")
    reward_date: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc))

    reward: Reward = Relationship(back_populates="history")
    student: Student = Relationship(back_populates="rewards_history", cascade_delete=True)



