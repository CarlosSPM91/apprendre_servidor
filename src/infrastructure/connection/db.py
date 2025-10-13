"""
Database connection utilities.

Provides the configuration and helpers to create the database engine
(SQLAlchemy/SQLModel) and initialize the schema. Also exposes a function
to generate asynchronous database sessions for FastAPI.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from ...settings import settings


def get_engine():
    """
    Create and return the asynchronous database engine.

    Returns:
        AsyncEngine: Database engine instance.

    :author: Carlos S. Paredes Morillo
    """
    return create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )


async def async_init_db(engine):
    """
    Initialize the database schema asynchronously.

    Imports all entity models and creates tables if they do not exist.

    Args:
        engine (AsyncEngine): The asynchronous database engine.
    """
    # Users
    from src.infrastructure.entities.users.roles import Role
    from src.infrastructure.entities.users.user import User
    from src.infrastructure.entities.users.accces_logs import AccessLog
    from src.infrastructure.entities.users.deletion_logs import DeletionLog
    from src.infrastructure.entities.users.professor import Professor
    from src.infrastructure.entities.users.parents import Parent

    # Student
    from src.infrastructure.entities.student_info.student_medical_info import StudentMedicalInfo
    from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
    from src.infrastructure.entities.student_info.student_intolerance import StudentIntolerance
    from src.infrastructure.entities.student_info.medical_info import MedicalInfo
    from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
    from src.infrastructure.entities.student_info.student_allergy import StudentAllergy
    from src.infrastructure.entities.student_info.student import Student

    # Course
    from src.infrastructure.entities.course.course import Course
    from src.infrastructure.entities.course.activity_type import ActivityType
    from src.infrastructure.entities.course.calendary_activity import CalendarActivity
    from src.infrastructure.entities.course.class_common_activity import ClassCommonActivity
    from src.infrastructure.entities.course.school_subject import SchoolSubject
    from src.infrastructure.entities.course.student_class import StudentClass
    from src.infrastructure.entities.course.subject_activity import SubjectActivity
    from src.infrastructure.entities.course.subject_activity_score import SubjectActivityScore
    from src.infrastructure.entities.course.subject_class import SubjectClass

    # Quiz
    from src.infrastructure.entities.quiz.quiz import Quiz
    from src.infrastructure.entities.quiz.quizz_response import QuizResponse
    from src.infrastructure.entities.quiz.reward import Reward
    from src.infrastructure.entities.quiz.reward_history import RewardHistory

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session(engine):
    """
    Generate an asynchronous database session for use with FastAPI dependencies.

    Args:
        engine (AsyncEngine): The asynchronous database engine.

    Yields:
        AsyncSession: A session to interact with the database.
    """
    async with AsyncSession(engine) as session:
        yield session
