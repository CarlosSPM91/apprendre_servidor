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
from src.application.use_case.auth.logout_use_case import LogoutUseCase
from src.application.use_case.role.create_role_case import CreateRoleCase
from src.application.use_case.role.delete_role_case import DeleteRoleCase
from src.application.use_case.role.find_role_case import FindRoleCase
from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.application.use_case.user.create_user_case import CreateUserCase
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.infrastructure.connection.db import get_engine, get_session
from src.infrastructure.connection.redis import get_redis_client, get_redis_session
from src.infrastructure.controllers.auth import AuthController
from src.infrastructure.controllers.role import RoleController
from src.infrastructure.controllers.user import UserController
from src.infrastructure.repositories.acces_logs import AccessRepository
from src.infrastructure.repositories.deletion_logs import DeletionRepository
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository
from src.settings import settings


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
    redis_client = providers.Singleton(get_redis_client)
    redis_session = providers.Factory(get_redis_session)
    config = providers.Object(settings)

    # Repositories
    user_repository = providers.Factory(UserRepository, session=session.provider)
    role_repository = providers.Factory(RoleRepository, session=session.provider)
    access_repository = providers.Factory(AccessRepository, session=session.provider)
    deletion_repository = providers.Factory(
        DeletionRepository, session=session.provider
    )

    find_user_case = providers.Factory(FindUserCase, repo=user_repository)

    # Services
    pwd_service = providers.Factory(PasswordService)
    token_service = providers.Factory(
        TokenService,
        find_case=find_user_case,
        redis_session=redis_session.provider,
        jwt_secret=config.provided.secret_key,
        jwt_algorithm=config.provided.algorithm,
        jwt_expiration=config.provided.duration,
    )

    # Use case
    create_user_case = providers.Factory(
        CreateUserCase, repo=user_repository, pwd_service=pwd_service
    )
    delete_user_case = providers.Factory(
        DeleteUserCase,
        repo=user_repository,
        find_user_case=find_user_case,
        deletion_repo=deletion_repository,
    )
    update_user_case = providers.Factory(
        UpdateUserCase, repo=user_repository, pwd_service=pwd_service
    )
    login_user_case = providers.Factory(
        LoginUseCase,
        find_case=find_user_case,
        update_case=update_user_case,
        pwd_service=pwd_service,
        token_service=token_service,
        access_repository=access_repository,
    )
    logout_user_case = providers.Factory(
        LogoutUseCase,
        token_service=token_service,
    )
    find_role_case = providers.Factory(FindRoleCase, role_repo=role_repository)
    create_role_case = providers.Factory(CreateRoleCase, role_repo=role_repository)
    delete_role_case = providers.Factory(DeleteRoleCase, role_repo=role_repository)
    update_role_case = providers.Factory(UpdateRoleCase, role_repo=role_repository)
    # Controllers
    user_controller = providers.Factory(
        UserController,
        find_case=find_user_case,
        create_case=create_user_case,
        update_case=update_user_case,
        delete_case=delete_user_case,
    )

    role_controller = providers.Factory(
        RoleController,
        find_role_case=find_role_case,
        create_role_case=create_role_case,
        update_role_case=update_role_case,
        delete_role_case=delete_role_case,
    )

    auth_controller = providers.Factory(
        AuthController, login_case=login_user_case, logout_case=logout_user_case
    )
