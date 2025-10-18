from sqlite3 import IntegrityError
from typing import Callable

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.student_info.student_allergy import StudentAllergy
from src.infrastructure.entities.student_info.student_intolerance import (
    StudentIntolerance,
)
from src.infrastructure.entities.student_info.student_medical_info import (
    StudentMedicalInfo,
)
from src.infrastructure.entities.users.user import User


class StudentRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get_student(self, student_id: int) -> Student:
        try:
            async for session in self.session():
                return (
                    await session.exec(select(Student).where(Student.id == student_id))
                ).first()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_student_full_info(self, student_id: int) -> StudentInfoDTO:
        try:
            async for session in self.session():
                result = (
                    await session.exec(
                        select(Student, User)
                        .join(User, Student.user_id == User.id)
                        .where(Student.id == student_id)
                    )
                ).first()
                student: Student
                user: User
                student, user = result
                return StudentInfoDTO(
                    student_id=student.id,
                    user_id=student.user_id,
                    name=user.name,
                    last_name=user.last_name,
                    obvervations=student.observations,
                )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, student: Student) -> Student:
        try:
            created = Student(
                user_id=student.user_id,
                observations=student.observations,
            )
            async for session in self.session():
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
        """
        Actualiza la información de un estudiante de forma segura y eficiente.

        Args:
            uptStudent: DTO con los datos a actualizar

        Returns:
            Student: Estudiante actualizado

        Raises:
            HTTPException: Si el estudiante no existe o hay error de integridad
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
                    for allergy in uptStudent.allergies:
                        session.add(
                            StudentAllergy(
                                students_user_id=student.id, allergy_info_id=allergy
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

    async def delete(self, uptStudent: Student) -> bool:
        try:
            async for session in self.session():
                student: Student = (
                    await session.exec(
                        select(Student).where(Student.id == uptStudent.id)
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
