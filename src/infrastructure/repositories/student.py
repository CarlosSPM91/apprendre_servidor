from sqlite3 import IntegrityError
from typing import Callable, List

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.student_info.student_allergy import StudentAllergy
from src.infrastructure.entities.student_info.student_intolerance import (
    StudentIntolerance,
)
from src.infrastructure.entities.student_info.student_medical_info import (
    StudentMedicalInfo,
)
from src.infrastructure.entities.users.user import User

"""
Students Repository.

Implements data access methods for the Student entity.

:author: Carlos S. Paredes Morillo
"""

class StudentRepository:
    """Repository for managing Student persistence.

    Provides CRUD operations and auxiliary methods
    for interacting with the Student entity in the database.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        self.session = session

    async def get_student(self, student_id: int) -> Student:
        """Retrieve a student by ID.

        Args:
            student_id (int): The ID of the student.

        Returns:
            Student: The student entity.

        Raises:
            HTTPException: If the student is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                selected = (
                    await session.exec(select(Student).where(Student.id == student_id))
                ).first()
                if not selected:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Student not found",
                    )
                return selected
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
    
    async def get_all(self) -> List[Student]:
        """Retrieve all students.

        Returns:
            List[Student]: A list of student entities.

        Raises:
            HTTPException: If no students are found or a database error occurs.
        """
        try:
            async for session in self.session():
                selected = (
                    await session.exec(select(Student))
                ).all()
                if not selected:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Students not found",
                    )
                return selected
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_student_full_info(self, student_id: int) -> StudentInfoDTO:
        """Retrieve full information of a student, including user info, allergies, intolerances, and medical info.

        Args:
            student_id (int): The ID of the student.

        Returns:
            StudentInfoDTO: Full student information.

        Raises:
            HTTPException: If the student is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                student_result = (
                    await session.exec(
                        select(Student, User)
                        .join(User, Student.user_id == User.id)
                        .where(Student.id == student_id)
                    )
                ).first()
                if not student_result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Student not found",
                    )
                student: Student
                user: User
                student, user = student_result

                allergies_result = (
                    await session.exec(
                        select(AllergyInfo)
                        .join(
                            StudentAllergy,
                            StudentAllergy.allergies_info_id == AllergyInfo.id,
                        )
                        .where(StudentAllergy.students_user_id == student_id)
                    )
                ).all()

                intolerances_result = (
                    await session.exec(
                        select(FoodIntolerance)
                        .join(
                            StudentIntolerance,
                            StudentIntolerance.food_intolerance_id
                            == FoodIntolerance.id,
                        )
                        .where(StudentIntolerance.students_user_id == student_id)
                    )
                ).all()

                medical_result = (
                    await session.exec(
                        select(MedicalInfo)
                        .join(
                            StudentMedicalInfo,
                            StudentMedicalInfo.medical_info_id == MedicalInfo.id,
                        )
                        .where(StudentMedicalInfo.students_user_id == student_id)
                    )
                ).all()

                return StudentInfoDTO(
                    student_id=student.id,
                    user_id=student.user_id,
                    name=user.name,
                    last_name=user.last_name,
                    email=user.email,
                    phone=user.phone,
                    classe="to improve",
                    obvervations=student.observations,
                    medical_info=medical_result,
                    allergies=allergies_result,
                    food_intolerance=intolerances_result,
                )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, student: Student) -> Student:
        """Create a new student.

        Args:
            student (Student): The student entity to create.

        Returns:
            Student: The created student.

        Raises:
            HTTPException: If the student already exists or a database error occurs.
        """
        try:
            created = Student(
                user_id=student.user_id,
                observations=student.observations,
            )
            async for session in self.session():
                exists = (
                    await session.exec(
                        select(Student).where(Student.user_id == student.user_id)
                    )
                ).first()
                if exists:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Student already exist",
                    )
                session.add(created)
                await session.commit()
                await session.refresh(created)
                return created

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def update(self, uptStudent: StudentUpdateDTO) -> Student:
        """Update a student's information, including allergies, intolerances, and medical info.

        Args:
            uptStudent (StudentUpdateDTO): Data for updating the student.

        Returns:
            Student: The updated student entity.

        Raises:
            HTTPException: If the student is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                student: Student = (
                    await session.exec(
                        select(Student).where(Student.id == uptStudent.student_id)
                    )
                ).first()
                if not student:
                    raise HTTPException(status_code=404, detail="Student not found")

                if uptStudent.observations is not None:
                    student.observations = uptStudent.observations

                if uptStudent.medical_info is not None:
                    await session.exec(
                        delete(StudentMedicalInfo).where(
                            StudentMedicalInfo.students_user_id == student.id
                        )
                    )
                    for med_id in uptStudent.medical_info:
                        session.add(
                            StudentMedicalInfo(
                                students_user_id=student.id, medical_info_id=med_id
                            )
                        )
                if uptStudent.allergies is not None:
                    await session.exec(
                        delete(StudentAllergy).where(
                            StudentAllergy.students_user_id == student.id
                        )
                    )
                    for allergy_id in uptStudent.allergies:
                        session.add(
                            StudentAllergy(
                                students_user_id=student.id,
                                allergies_info_id=allergy_id,
                            )
                        )

                if uptStudent.food_intolerance is not None:
                    await session.exec(
                        delete(StudentIntolerance).where(
                            StudentIntolerance.students_user_id == student.id
                        )
                    )
                    for intolerance in uptStudent.food_intolerance:
                        session.add(
                            StudentIntolerance(
                                students_user_id=student.id,
                                food_intolerance_id=intolerance,
                            )
                        )

                session.add(student)
                await session.commit()
                await session.refresh(student)
                return student

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def delete(self, student_id: int) -> bool:
        """Delete a student by ID.

        Args:
            student_id (int): The ID of the student.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the student is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                student: Student = (
                    await session.exec(
                        select(Student).where(Student.id == student_id)
                    )
                ).first()

                if not student:
                    raise HTTPException(status_code=404, detail="Student not found")
                await session.delete(student)
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
