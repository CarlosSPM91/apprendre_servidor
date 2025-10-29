from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.course import CourseController
from src.infrastructure.entities.course.course import Course
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/courses", tags=["course"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all courses",
    response_description="Returns a list of all courses",
)
@inject
async def find_all(
    controller: CourseController = Depends(Provide[Container.course_controller]),
):
    return await controller.get_all()


@router.get(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of acourses",
    response_description="Returns the information of a courses",
)
@inject
async def find(
    course_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CourseController = Depends(Provide[Container.course_controller]),
):
    return await controller.get(course_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a courses",
    response_description="Returns the information of a courses",
)
@inject
async def create(
    payload: Course,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CourseController = Depends(Provide[Container.course_controller]),
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
    payload: Course,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CourseController = Depends(Provide[Container.course_controller]),
):
    return await controller.update(payload)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    name="delete-course",
    summary="Delete a course",
    response_description="Returns the deleted course id",
)
@inject
async def delete(
    course_id: int,
    controller: CourseController = Depends(Provide[Container.course_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(course_id)
