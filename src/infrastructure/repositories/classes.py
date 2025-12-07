from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.classes.class_subjects_dto import ClassSubjectsDTO
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.entities.course.subject_class import SubjectClass

"""
Classes Repository.

Implements data access methods for the Classes entity and its associated subjects.

:author: Carlos S. Paredes Morillo
"""

class ClassesRepository:
    """Repository for managing Classes persistence.

    Provides CRUD operations and auxiliary methods for interacting with
    Classes and their associated subjects.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, classes: Classes) -> Classes:
        """Create a new class.

        Args:
            classes (Classes): The class entity to create.

        Returns:
            Classes: The created class.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
        try:
            async for session in self.session():
                session.add(classes)
                await session.commit()
                await session.refresh(classes)
                return classes
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self) -> List[Classes]:
        """Retrieve all classes.

        Returns:
            List[Classes]: A list of class entities.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            async for session in self.session():
                classes: List[Classes] = (await session.exec(select(Classes))).all()
                return classes
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_by_id(self, class_id: int) -> ClassSubjectsDTO:
        """Retrieve a class by ID along with its associated subjects.

        Args:
            class_id (int): The ID of the class.

        Returns:
            ClassSubjectsDTO: Class details and associated subject IDs.

        Raises:
            HTTPException: If the class is not found.
        """
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == class_id))
            ).first()
            if not classes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Classes not found"
                )

            subjects = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.class_id == classes.id)
                )
            ).all()

            return ClassSubjectsDTO(
                id=classes.id,
                course_id=classes.course_id,
                name=classes.name,
                tutor_id=classes.tutor_id,
                subjects=[subject.subject_id for subject in subjects],
            )

    async def update(self, classes_upt: Classes) -> Optional[Classes]:
        """Update a class's details.

        Args:
            classes_upt (Classes): Class entity with updated fields.

        Returns:
            Optional[Classes]: The updated class, or None if not found.

        Raises:
            HTTPException: If the class is not found or a database integrity error occurs.
        """
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == classes_upt.id))
            ).first()

            if classes is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Classes not found",
                )

            if classes_upt.course_id is not None:
                classes.course_id = classes_upt.course_id
            if classes_upt.tutor_id is not None:
                classes.tutor_id = classes_upt.tutor_id
            if classes_upt.name is not None:
                classes.name = classes_upt.name

            try:
                session.add(classes)
                await session.commit()
                await session.refresh(classes)
                return classes
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def update_subjects(self, subjects: UpdateClassSubjectsDTO) -> Optional[ClassSubjectsDTO]:
        """Update the subjects associated with a class.

        Args:
            subjects (UpdateClassSubjectsDTO): DTO containing class ID and new subjects.

        Returns:
            Optional[ClassSubjectsDTO]: Updated class details and subject IDs.

        Raises:
            HTTPException: If the class is not found or a database integrity error occurs.
        """
        async for session in self.session():
            classes: Classes = (
                await session.exec(
                    select(Classes).where(Classes.id == subjects.class_id)
                )
            ).first()

            if classes is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Class not found",
                )
            try:
                await session.exec(
                    delete(SubjectClass).where(SubjectClass.class_id == classes.id)
                )
                for subject in subjects.subjects:
                    session.add(
                        SubjectClass(
                            subject_id=subject.subject_id,
                            class_id=classes.id,
                            professor_id=subject.teacher_id,
                        )
                    )
                session.add(classes)
                await session.commit()
                await session.refresh(classes)

                updated_subjects = (
                    await session.exec(
                        select(SubjectClass).where(SubjectClass.class_id == classes.id)
                    )
                ).all()

                return ClassSubjectsDTO(
                    id=classes.id,
                    course_id=classes.course_id,
                    name=classes.name,
                    tutor_id=classes.tutor_id,
                    subjects=[subject.subject_id for subject in updated_subjects],
                )
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, classes_id: int) -> bool:
        """Delete a class by ID.

        Args:
            classes_id (int): The ID of the class to delete.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the class is not found or a database integrity error occurs.
        """
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == classes_id))
            ).first()
            if not classes:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classes not found")

            try:
                await session.delete(classes)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Classes already in use. Foreign key constraint violation.",
                )
