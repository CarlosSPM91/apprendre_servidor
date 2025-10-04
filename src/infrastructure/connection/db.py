"""
Database connection utilities.

Provides the configuration and helpers to create the database engine
(SQLAlchemy/SQLModel) and initialize the schema. Also exposes a function
to generate asynchronous database sessions for FastAPI.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from ...settings import settings


def get_engine():
    """Create and return the asynchronous database engine.

    Returns:
        AsyncEngine: Database engine instance.

    :author: Carlos S. Paredes Morillo
    """
    return create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

# async def get_session_maker(engine):
#     SessionLocal = sessionmaker(
#         autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
#     )


async def async_init_db(engine):

    from src.infrastructure.entities.user import User
    from src.infrastructure.entities.roles import Role
    from src.infrastructure.entities.accces_logs import AccesLog
    from src.infrastructure.entities.deletion_logs import DeletionLog

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        pass


async def get_session(engine):
    async with AsyncSession(engine) as session:
        yield session
