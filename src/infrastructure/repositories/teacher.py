from sqlite3 import IntegrityError
from typing import Callable, List

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.domain.objects.profiles.teacher_update_dto import TeacherUpdateDTO
from src.domain.objects.subject_dto import SubjectDTO
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.entities.users.teacher import Teacher
from src.infrastructure.entities.users.user import User

"""
Teachers Repository.

Implements data access methods for the Teacher entity.

:author: Carlos S. Paredes Morillo
"""

class TeacherRepository:
    """Repository for managing Teacher persistence.

    Provides CRUD operations and auxiliary methods
    for interacting with the Teacher entity in the database.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        self.session = session

    async def get_teacher(self, teacher_id: int):
        """Retrieve a teacher by ID.

        Args:
            teacher_id (int): The ID of the teacher.

        Returns:
            Teacher: The teacher entity.

        Raises:
            HTTPException: If the teacher is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                selected = (
                    await session.exec(select(Teacher).where(Teacher.id == teacher_id))
                ).first()
                if not selected:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Teacher not found",
                    )
                return selected
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_teacher_full_info(self, teacher_id: int):
        """Retrieve full information of a teacher, including user info and subjects.

        Args:
            teacher_id (int): The ID of the teacher.

        Returns:
            TeacherDTO: The teacher data transfer object with related subjects.

        Raises:
            HTTPException: If the teacher is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                selected = (
                    await session.exec(
                        select(Teacher, User)
                        .join(User, Teacher.user_id == User.id)
                        .where(Teacher.id == teacher_id)
                    )
                ).first()
                if not selected:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Teacher not found",
                    )
                teacher: Teacher
                user: User
                teacher, user = selected

                subjects_result = (
                    await session.exec(
                        select(SubjectClass, SchoolSubject)
                        .join(
                            SchoolSubject, SubjectClass.subject_id == SchoolSubject.id
                        )
                        .where(SubjectClass.professor_id == teacher_id)
                    )
                ).all()

                subjects = [
                    SubjectDTO(
                        subject_id=school_subject.id,
                        subject_name=school_subject.name,
                        subject_class=subject_class.class_id,
                        description=school_subject.description,
                    )
                    for subject_class, school_subject in subjects_result
                ]

                return TeacherDTO(
                    user_id=user.id,
                    teacher_id=teacher.id,
                    name=user.name,
                    last_name=user.last_name,
                    dni=user.dni,
                    phone=user.phone,
                    email=user.email,
                    username=user.username,
                    subjects=subjects,
                )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self):
        """Retrieve all teachers with their user info and subjects.

        Returns:
            List[TeacherDTO]: A list of teachers.

        Raises:
            HTTPException: If no teachers are found or a database error occurs.
        """
        try:
            async for session in self.session():
                teachers_users = (
                    await session.exec(
                        select(Teacher, User).join(User, Teacher.user_id == User.id)
                    )
                ).all()
                if teachers_users is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Teachers not found",
                    )
                teacher_ids = [teacher.id for teacher, _ in teachers_users]
                all_subjects = (
                    await session.exec(
                        select(SubjectClass, SchoolSubject, SubjectClass.professor_id)
                        .join(
                            SchoolSubject, SubjectClass.subject_id == SchoolSubject.id
                        )
                        .where(SubjectClass.professor_id.in_(teacher_ids))
                    )
                ).all()

                subjects_by_teacher = {}
                for subject_class, school_subject, professor_id in all_subjects:
                    if professor_id not in subjects_by_teacher:
                        subjects_by_teacher[professor_id] = []

                    subjects_by_teacher[professor_id].append(
                        SubjectDTO(
                            subject_id=school_subject.id,
                            subject_name=school_subject.name,
                            subject_class=subject_class.class_id,
                            description=school_subject.description,
                        )
                    )

                teachers_dto = []
                for teacher, user in teachers_users:
                    teachers_dto.append(
                        TeacherDTO(
                            user_id=user.id,
                            teacher_id=teacher.id,
                            name=user.name,
                            last_name=user.last_name,
                            dni=user.dni,
                            phone=user.phone,
                            email=user.email,
                            username=user.username,
                            subjects=subjects_by_teacher.get(teacher.id, []),
                        )
                    )

                return teachers_dto
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, user_id: int):
        """Create a new teacher.

        Args:
            user_id (int): The ID of the associated user.

        Returns:
            Teacher: The created teacher entity.

        Raises:
            HTTPException: If the teacher already exists or a database error occurs.
        """
        try:
            created = Teacher(user_id=user_id)
            async for session in self.session():

                exists = (
                    await session.exec(
                        select(Teacher).where(Teacher.user_id == user_id)
                    )
                ).first()
                if exists:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Teacher already exist",
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

    async def delete(self, teacher_id: int):
        """Delete a teacher by ID.

        Args:
            teacher_id (int): The ID of the teacher to delete.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the teacher is not found or a database error occurs.
        """
        try:
            async for session in self.session():
                teacher: Teacher = (
                    await session.exec(select(Teacher).where(Teacher.id == teacher_id))
                ).first()

                if not teacher:
                    raise HTTPException(status_code=404, detail="Teacher not found")
                await session.delete(teacher)
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
