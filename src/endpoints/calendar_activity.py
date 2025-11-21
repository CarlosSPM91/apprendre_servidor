from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.calendar_activity import CalendarController
from src.infrastructure.controllers.course import CourseController
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.entities.course.course import Course
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all calendar activities",
    response_description="Returns a list of all calendar activities",
)
@inject
async def find_all(
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    return await controller.get_all()


@router.get(
    "/{calendar_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of acourses",
    response_description="Returns the information of a calendar activities",
)
@inject
async def find(
    calendar_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    return await controller.get(calendar_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a courses",
    response_description="Returns the information of a courses",
)
@inject
async def create(
    payload: CalendarActivity,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-course",
    summary="Update an existing course",
    response_description="Returns the updated course",
)
@inject
async def update(
    payload: CalendarActivity,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    return await controller.update(payload)


@router.delete(
    "/{calendar_id}",
    status_code=status.HTTP_200_OK,
    name="delete-calendar-activity",
    summary="Delete a calendar activities",
    response_description="Returns the deleted calendar activities id",
)
@inject
async def delete(
    course_id: int,
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(course_id)
