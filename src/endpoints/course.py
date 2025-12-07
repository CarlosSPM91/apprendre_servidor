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
    """Retrieve all courses in the system.

    Args:
        controller (CourseController): Controller handling course operations.

    Returns:
        list: List of Course objects.
    """
    return await controller.get_all()


@router.get(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of a course",
    response_description="Returns the information of a course",
)
@inject
async def find(
    course_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CourseController = Depends(Provide[Container.course_controller]),
):
    """Retrieve a single course by its ID.

    Args:
        course_id (int): ID of the course to retrieve.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CourseController): Controller handling course operations.

    Returns:
        dict: Course information.
    """
    return await controller.get(course_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a new course",
    response_description="Returns the information of the created course",
)
@inject
async def create(
    payload: Course,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CourseController = Depends(Provide[Container.course_controller]),
):
    """Create a new course in the system.

    Args:
        payload (Course): Payload containing course data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CourseController): Controller handling course operations.

    Returns:
        dict: Created course ID and creation timestamp.
    """
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
    """Update an existing course.

    Args:
        payload (Course): Payload containing updated course data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CourseController): Controller handling course operations.

    Returns:
        dict: Updated course ID and timestamp.
    """
    return await controller.update(payload)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    name="delete-course",
    summary="Delete a course",
    response_description="Returns the deleted course ID",
)
@inject
async def delete(
    course_id: int,
    controller: CourseController = Depends(Provide[Container.course_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Delete a course from the system by its ID.

    Args:
        course_id (int): ID of the course to delete.
        controller (CourseController): Controller handling course operations.
        current_user (JwtPayload): Authenticated user performing the deletion.

    Returns:
        dict: Deleted course ID and deletion timestamp.
    """
    return await controller.delete(course_id)
