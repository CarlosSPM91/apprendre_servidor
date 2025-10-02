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
    """Create and return the asynchronous database engine.

    Returns:
        AsyncEngine: Database engine instance.

    :author: Carlos S. Paredes Morillo
    """
    return create_async_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True,
    )

async def async_init_db(engine):
    """Initialize the database schema.

    Executes `SQLModel.metadata.create_all` using the provided engine.

    Args:
        engine (AsyncEngine): Database engine instance.

    :author: Carlos S. Paredes Morillo
    """
    from src.infrastructure.entities.user import User
    from src.infrastructure.entities.roles import Role
    from src.infrastructure.entities.accces_logs import AccesLog
    from src.infrastructure.entities.deletion_logs import DeletionLog
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session(engine):
    """Provide an asynchronous database session.

    Typically used as a FastAPI dependency to obtain a session
    per request.

    Args:
        engine (AsyncEngine): Database engine instance.

    Yields:
        AsyncSession: SQLAlchemy asynchronous session.

    :author: Carlos S. Paredes Morillo
    """
    async with AsyncSession(engine) as session:
        yield session
