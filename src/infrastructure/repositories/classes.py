from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.classes import Classes


class ClasesRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, classes: Classes):
        try:
            async for session in self.session():
                session.add(classes)
                await session.commit()
                await session.refreash(classes)
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
            if not classes:
                return []
            return classes

    async def get_by_id(self, class_id: int) -> Classes:
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == class_id))
            ).first()
            if not classes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
                )
            return classes

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

    async def delete(self, classes_id: int) -> bool:
        async for session in self.session():
            classes: Classes = (
                await session.exec(select(Classes).where(Classes.id == classes))
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
