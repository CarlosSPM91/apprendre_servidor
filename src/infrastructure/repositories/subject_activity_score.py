from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.subject_activity import SubjectActivity
from src.infrastructure.entities.course.subject_activity_score import SubjectActivityScore



class SubjectActivityScoreRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, activity: SubjectActivityScore):
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

    async def get_all(self, activity_score_id:int) -> List[SubjectActivityScore]:
        async for session in self.session():
            activities: List[SubjectActivityScore] = (
                await session.exec(select(SubjectActivityScore).where(SubjectActivityScore.subject_activity_id == activity_score_id))
            ).all()
            if not activities:
                return []
            return activities

    async def get(self, activity_score_id: int) -> SubjectActivityScore:
        async for session in self.session():
            activity_score: SubjectActivityScore = (
                await session.exec(
                    select(SubjectActivityScore).where(SubjectActivityScore.id == activity_score_id)
                )
            ).first()
            if not activity_score:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subject Activity Score not found",
                )
            return activity_score

    async def update_note(self, activity_score_upt: SubjectActivityScore) -> Optional[SubjectActivityScore]:
        async for session in self.session():
            activity_score: SubjectActivityScore = (
                await session.exec(select(SubjectActivityScore).where(SubjectActivityScore.id == activity_score_upt.id))
            ).first()

            if activity_score:
                if activity_score_upt.note is not None:
                    activity_score.note=activity_score_upt.note

                try:
                    session.add(activity_score)
                    await session.commit()
                    await session.refresh(activity_score)
                    return activity_score
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, activity_score_id: int) -> bool:
        async for session in self.session():
            activity_score: SubjectActivity = (
                await session.exec(
                    select(SubjectActivity).where(SubjectActivity.id == activity_score_id)
                )
            ).first()
            if not activity_score:
                raise HTTPException(status_code=404, detail="Subject Activity Score not found")

            try:
                await session.delete(activity_score)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Subject Activity Score already in use. Foreign key constraint violation.",
                )
