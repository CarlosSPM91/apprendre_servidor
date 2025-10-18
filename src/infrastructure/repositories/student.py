from sqlite3 import IntegrityError
from typing import Callable

from fastapi import HTTPException, status
from sqlmodel import select

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.infrastructure.entities.student_info.student import Student
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
                    await session.exec(select(Student, User).join(User, Student.user_id == User.id).where(Student.id == student_id))
                ).first()
                student:Student 
                user :User
                student,user= result
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

    async def update(self, uptStudent: Student) -> Student:
        try:
            async for session in self.session():
                student: Student = (
                    await session.exec(
                        select(Student).where(Student.id == uptStudent.id)
                    )
                ).first()

                for field, value in uptStudent.model_dump(exclude_unset=True).items():
                    if field != "id":
                        setattr(student, field, value)

                await session.add(student)
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
