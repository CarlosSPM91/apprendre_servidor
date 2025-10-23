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
from src.application.use_case.allergy_info.create_allergy_case import CreateAllergyCase
from src.application.use_case.allergy_info.delete_allergy_case import DeleteAllergyCase
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.application.use_case.allergy_info.update_allergy_case import UpdateAllergyCase
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.application.use_case.auth.logout_use_case import LogoutUseCase
from src.application.use_case.food_intolerance.create_intolerance_case import (
    CreateIntoleranceCase,
)
from src.application.use_case.food_intolerance.delete_intolerance_case import (
    DeleteIntoleranceCase,
)
from src.application.use_case.food_intolerance.find_intolerance_case import (
    FindIntoleranceCase,
)
from src.application.use_case.food_intolerance.update_intolerance_case import (
    UpdateIntoleranceCase,
)
from src.application.use_case.medical_info.create_medical_case import CreateMedicalCase
from src.application.use_case.medical_info.delete_medical_case import DeleteMedicalCase
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.application.use_case.medical_info.update_medical_case import UpdateMedicalCase
from src.application.use_case.parent.create_parent_case import CreateParentCase
from src.application.use_case.parent.delete_parent_case import DeleteParentCase
from src.application.use_case.parent.find_parent_case import FindParentCase
from src.application.use_case.role.create_role_case import CreateRoleCase
from src.application.use_case.role.delete_role_case import DeleteRoleCase
from src.application.use_case.role.find_role_case import FindRoleCase
from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.application.use_case.student.create_student_case import CreateStudenCase
from src.application.use_case.student.delete_student_case import DeleteStudentCase
from src.application.use_case.student.find_student_case import FindStudentCase
from src.application.use_case.student.update_student_case import UpdateStudentCase
from src.application.use_case.teacher.create_teacher_case import CreateTeacherCase
from src.application.use_case.teacher.delete_teacher_case import DeleteTeacherCase
from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.application.use_case.user.create_user_case import CreateUserCase
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.infrastructure.connection.db import get_engine, get_session
from src.infrastructure.connection.redis import get_redis_client, get_redis_session
from src.infrastructure.controllers.allergy_info import AllergyController
from src.infrastructure.controllers.auth import AuthController
from src.infrastructure.controllers.food_intolrance import FoodIntoleranceController
from src.infrastructure.controllers.medical_info import MedicalInfoController
from src.infrastructure.controllers.parent import ParentController
from src.infrastructure.controllers.role import RoleController
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.controllers.teacher import TeacherController
from src.infrastructure.controllers.user import UserController
from src.infrastructure.repositories.acces_logs import AccessRepository
from src.infrastructure.repositories.allergy_info import AllergyRepository
from src.infrastructure.repositories.deletion_logs import DeletionRepository
from src.infrastructure.repositories.food_intolerance import FoodIntoleranceRepository
from src.infrastructure.repositories.medical_info import MedicalInfoRepository
from src.infrastructure.repositories.parent import ParentRepository
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.student import StudentRepository
from src.infrastructure.repositories.teacher import TeacherRepository
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
    student_repository = providers.Factory(StudentRepository, session=session.provider)
    medical_info_repository = providers.Factory(
        MedicalInfoRepository, session=session.provider
    )
    intolerance_food_repository = providers.Factory(
        FoodIntoleranceRepository, session=session.provider
    )
    allergy_repository = providers.Factory(AllergyRepository, session=session.provider)
    parent_repository = providers.Factory(ParentRepository, session=session.provider)
    teacher_repository = providers.Factory(TeacherRepository, session=session.provider)

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
    find_role_case = providers.Factory(FindRoleCase, role_repo=role_repository)
    create_student_case = providers.Factory(CreateStudenCase, repo=student_repository)
    create_teacher_case = providers.Factory(
        CreateTeacherCase, repo=teacher_repository
    )
    create_user_case = providers.Factory(
        CreateUserCase,
        repo=user_repository,
        pwd_service=pwd_service,
        create_student_case=create_student_case,
        create_teacher_case=create_teacher_case,
        find_role_case=find_role_case,
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

    create_role_case = providers.Factory(CreateRoleCase, role_repo=role_repository)
    delete_role_case = providers.Factory(DeleteRoleCase, role_repo=role_repository)
    update_role_case = providers.Factory(UpdateRoleCase, role_repo=role_repository)
    find_student_case = providers.Factory(FindStudentCase, repo=student_repository)

    find_medical_case = providers.Factory(FindMedicalCase, repo=medical_info_repository)
    create_medical_case = providers.Factory(
        CreateMedicalCase, repo=medical_info_repository
    )
    update_medical_case = providers.Factory(
        UpdateMedicalCase, repo=medical_info_repository
    )
    delete_medical_case = providers.Factory(
        DeleteMedicalCase, repo=medical_info_repository, find_case=find_medical_case
    )

    find_allergy_case = providers.Factory(FindAllergyCase, repo=allergy_repository)
    create_allergy_case = providers.Factory(CreateAllergyCase, repo=allergy_repository)
    update_allergy_case = providers.Factory(UpdateAllergyCase, repo=allergy_repository)
    delete_allergy_case = providers.Factory(
        DeleteAllergyCase, repo=allergy_repository, find_case=find_allergy_case
    )

    find_intolerance_case = providers.Factory(
        FindIntoleranceCase, repo=intolerance_food_repository
    )
    create_intolerance_case = providers.Factory(
        CreateIntoleranceCase, repo=intolerance_food_repository
    )
    update_intolerance_case = providers.Factory(
        UpdateIntoleranceCase, repo=intolerance_food_repository
    )
    delete_intolerance_Case = providers.Factory(
        DeleteIntoleranceCase,
        repo=intolerance_food_repository,
        find_case=find_intolerance_case,
    )

    update_student_case = providers.Factory(UpdateStudentCase, repo=student_repository)
    delete_student_case = providers.Factory(
        DeleteStudentCase,
        repo=student_repository,
        find_student_case=find_student_case,
    )

    find_parent_case = providers.Factory(
        FindParentCase, repo=parent_repository, find_user=find_user_case
    )
    create_parent_case = providers.Factory(
        CreateParentCase, repo=parent_repository
    )
    delete_parent_case = providers.Factory(
        DeleteParentCase,
        repo=parent_repository,
    )

    find_teacher_case = providers.Factory(
        FindTeacherCase, repo=teacher_repository
    )
    
    delete_teacher_case = providers.Factory(
        DeleteTeacherCase,
        repo=teacher_repository,
        find_case=find_teacher_case
    )
    
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

    student_contoller = providers.Factory(
        StudentController,
        find_case=find_student_case,
        create_case=create_student_case,
        update_case=update_student_case,
        delete_case=delete_student_case,
    )

    medical_info_controller = providers.Factory(
        MedicalInfoController,
        find_case=find_medical_case,
        create_case=create_medical_case,
        update_case=update_medical_case,
        delete_case=delete_medical_case,
    )

    food_intolerance_controller = providers.Factory(
        FoodIntoleranceController,
        find_case=find_intolerance_case,
        create_case=create_intolerance_case,
        update_case=update_intolerance_case,
        delete_case=delete_intolerance_Case,
    )

    allergy_controller = providers.Factory(
        AllergyController,
        find_case=find_allergy_case,
        create_case=create_allergy_case,
        update_case=update_allergy_case,
        delete_case=delete_allergy_case,
    )

    parent_controller = providers.Factory(
        ParentController,
        find_case=find_parent_case,
        create_case=create_parent_case,
        delete_case=delete_parent_case,
    )

    teacher_controller = providers.Factory(
        TeacherController,
        find_case=find_teacher_case,
        create_case=create_teacher_case,
        delete_case=delete_teacher_case,
    )

    auth_controller = providers.Factory(
        AuthController, login_case=login_user_case, logout_case=logout_user_case
    )
