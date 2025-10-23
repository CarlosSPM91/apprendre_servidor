"""
Create User Use Case.

Handles the creation of new users, including password hashing
and duplicate username checks.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.application.use_case.role.find_role_case import FindRoleCase
from src.application.use_case.student.create_student_case import CreateStudenCase
from src.application.use_case.teacher.create_teacher_case import CreateTeacherCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.repositories.user import UserRepository


class CreateUserCase:
    """Use case for creating new users in the system."""

    def __init__(
        self,
        pwd_service: PasswordService,
        repo: UserRepository,
        create_student_case: CreateStudenCase,
        create_teacher_case: CreateTeacherCase,
        find_role_case:FindRoleCase
    ):
        """
        Initialize the CreateUserCase with required services and repository.

        Args:
            pwd_service (PasswordService): Service for hashing passwords.
            repo (UserRepository): Repository for user persistence.
        """
        self.pwdService = pwd_service
        self.userRepo = repo
        self.create_student_case = create_student_case
        self.create_teacher_case = create_teacher_case
        self.find_role_case = find_role_case

    async def create(self, payload: UserCreateDTO) -> CommonResponse:
        """
        Create a new user, ensuring the username is unique and hashing the password.

        Args:
            payload (UserCreateDTO): Data transfer object containing user information.

        Returns:
            CommonResponse: Response containing the new user's ID and the event timestamp.

        Raises:
            HTTPException: If the username already exists (HTTP 409 Conflict).
        """
        user_check = await self.userRepo.get_user_by_username(payload.username)
        if user_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exist"
            )

        pwd_hash = self.pwdService.hash_password(payload.password)
        payload.password = pwd_hash

        user_created = await self.userRepo.create(payload)
        roles = await self.find_role_case.get_all()
        roles_dict = {r.role_id: r.role_name for r in roles}

        match user_created.role:
            case 1: 
                if roles_dict.get(1, "").lower() == "admin":
                    pass
                else:
                    raise HTTPException(status_code=400, detail="Invalid role mapping for Admin")

            case 2: 
                if roles_dict.get(2, "").lower() == "teacher":
                    await self.create_teacher_case.create(user_id=user_created.user_id)
                else:
                    raise HTTPException(status_code=400, detail="Invalid role mapping for Teacher")

            case 3: 
                if roles_dict.get(3, "").lower() == "student":
                    student = Student(
                        user_id=user_created.user_id,  
                    )
                    await self.create_student_case.create(student)
                else:
                    raise HTTPException(status_code=400, detail="Invalid role mapping for Student")

            case 4: 
                if roles_dict.get(4, "").lower() == "parent":
                    pass
                else:
                    raise HTTPException(status_code=400, detail="Invalid role mapping for Parent")

            case _:
                raise HTTPException(status_code=400, detail="Role not valid")
    
            
        return CommonResponse(
            item_id=user_created.user_id, event_date=datetime.now(timezone.utc)
        )
