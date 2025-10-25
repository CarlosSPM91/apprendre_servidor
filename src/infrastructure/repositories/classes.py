from sqlite3 import IntegrityError
from typing import Callable, Dict, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.classes.class_subjects_dto import ClassSubjectsDTO
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.entities.course.subject_class import SubjectClass


class ClassesRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, classes: Classes):
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
        async for session in self.session():
            classes: List[Classes] = (await session.exec(select(Classes))).all()
            return classes

    async def get_by_id(self, class_id: int) -> ClassSubjectsDTO:
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == class_id))
            ).first()
            if not classes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
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
                student_class_id=classes.student_class_id,
                tutor_id=classes.tutor_id,
                subjects=[subject.subject_id for subject in subjects],
            )

    async def update(self, classes_upt: Classes) -> Optional[Classes]:
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == classes.id))
            ).first()

            if classes:
                if classes_upt.tutor_id is not None:
                    classes.tutor_id = classes_upt.tutor_id

                if classes_upt.student_class_id is not None:
                    classes.student_class_id = classes_upt.student_class_id

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
            return None

    async def update_subjects(
        self, subjects: UpdateClassSubjectsDTO
    ) -> Optional[ClassSubjectsDTO]:
        async for session in self.session():
            classes: Classes = (
                await session.exec(
                    select(Classes).where(Classes.id == subjects.class_id)
                )
            ).first()

            try:
                if classes:
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

                    subjects = (
                        await session.exec(
                            select(SubjectClass).where(
                                SubjectClass.class_id == classes.id
                            )
                        )
                    ).all()

                    return ClassSubjectsDTO(
                        id=classes.id,
                        course_id=classes.course_id,
                        name=classes.name,
                        student_class_id=classes.student_class_id,
                        tutor_id=classes.tutor_id,
                        subjects=[subject.subject_id for subject in subjects],
                    )
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, classes_id: int) -> bool:
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == classes_id))
            ).first()
            if not classes:
                raise HTTPException(status_code=404, detail="Classes not found")

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
