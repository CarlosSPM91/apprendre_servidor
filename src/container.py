"""
Dependency Injection Container.

Defines the dependency-injection container using the `dependency-injector`
library. Provides singletons and factories for the database engine, sessions,
repositories, and application services.

:author: Carlos S. Paredes Morillo
"""

from dependency_injector import containers, providers
from src.application.services.password_service import PasswordService
from src.application.services.token_service import TokenService
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.application.use_case.user.create_user_case import CreateUserCase
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
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
    session = providers.Factory(get_session, engine=database_engine)

    # Repositories
    user_repository = providers.Factory(UserRepository, session=session)

    find_user_case = providers.Factory(FindUserCase, repo=user_repository)

    # Services
    pwd_service = providers.Factory(PasswordService)
    token_service = providers.Factory(TokenService, find_case=find_user_case)

    # Use case
    create_user_case = providers.Factory(
        CreateUserCase, repo=user_repository, pwd_service=pwd_service
    )
    delete_user_case = providers.Factory(DeleteUserCase, repo=user_repository)
    update_user_case = providers.Factory(
        UpdateUserCase, repo=user_repository, pwd_service=pwd_service
    )
    login_user_case = providers.Factory(
        LoginUseCase,
        update_case=update_user_case,
        pwd_service=pwd_service,
        token_service=token_service,
    )
