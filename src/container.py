"""
Dependency Injection Container.

Defines the dependency-injection container using the `dependency-injector`
library. Provides singletons and factories for the database engine, sessions,
repositories, and application services.

:author: Carlos S. Paredes Morillo
"""
from dependency_injector import containers, providers
from src.application.services.user import UserService
from src.infrastructure.connection.db import get_engine, get_session
from src.infrastructure.repositories.user import UserRepository


class Container(containers.DeclarativeContainer):
    """Main dependency-injection container.

    Manages the creation and injection of core components:
      - Database engine (Singleton).
      - Database sessions (Factory).
      - Repositories (Factory).
      - Application services (Factory).

    This container is wired with FastAPI to provide dependencies
    directly to the endpoints.

    :author: Carlos S. Paredes Morillo
    """
    database_engine = providers.Singleton(get_engine)
    session = providers.Factory(get_session, engine = database_engine)
    
    user_repository = providers.Factory(UserRepository, session= session)
    user_service = providers.Factory(UserService, repo=user_repository)
