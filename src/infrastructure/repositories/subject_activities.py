from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.subject_activity import SubjectActivity



class SubjectActivityRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, activity: SubjectActivity):
        try:
            async for session in self.session():
                session.add(activity)
                await session.commit()
                await session.refreash(activity)
                return activity

        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self, subject_class_id:int) -> List[SubjectActivity]:
        async for session in self.session():
            activities: List[SubjectActivity] = (
                await session.exec(select(SubjectActivity).where(SubjectActivity.subject_class_id == subject_class_id))
            ).all()
            if not activities:
                return []
            return activities

    async def get(self, activity_id: int) -> SubjectActivity:
        async for session in self.session():
            activity: SubjectActivity = (
                await session.exec(
                    select(SubjectActivity).where(SubjectActivity.id == activity_id)
                )
            ).first()
            if not activity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subject Activity not found",
                )
            return activity_id

    async def update(self, activity_upt: SubjectActivity) -> Optional[SubjectActivity]:
        async for session in self.session():
            activity: SubjectActivity = (
                await session.exec(select(SubjectActivity).where(SubjectActivity.id == activity_upt.id))
            ).first()

            if activity:
                if activity_upt.name is not None:
                    activity.name=activity_upt.name
                if activity_upt.activity_type_id is not None:
                    activity.activity_type_id=activity_upt.activity_type_id

                try:
                    session.add(activity)
                    await session.commit()
                    await session.refresh(activity)
                    return activity
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, activity_id: int) -> bool:
        async for session in self.session():
            student_class: SubjectActivity = (
                await session.exec(
                    select(SubjectActivity).where(SubjectActivity.id == activity_id)
                )
            ).first()
            if not student_class:
                raise HTTPException(status_code=404, detail="Subject Activity not found")

            try:
                await session.delete(student_class)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Subject Activity already in use. Foreign key constraint violation.",
                )
