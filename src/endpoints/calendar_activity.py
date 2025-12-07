from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.calendar_activity import CalendarController
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.middleware.token.authenticateToken import get_current_user

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find_all",
    summary="Get all calendar activities",
    response_description="Returns a list of all calendar activities",
)
@inject
async def find_all(
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    """Retrieve all calendar activities in the system.

    Args:
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CalendarController): Controller handling calendar activity operations.

    Returns:
        list: List of CalendarActivity objects.
    """
    return await controller.get_all()


@router.get(
    "/{calendar_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get a calendar activity by ID",
    response_description="Returns the information of a calendar activity",
)
@inject
async def find(
    calendar_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    """Retrieve a single calendar activity by its ID.

    Args:
        calendar_id (int): ID of the calendar activity to retrieve.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CalendarController): Controller handling calendar activity operations.

    Returns:
        dict: Calendar activity information.
    """
    return await controller.get(calendar_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a new calendar activity",
    response_description="Returns the information of the created calendar activity",
)
@inject
async def create(
    payload: CalendarActivity,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    """Create a new calendar activity in the system.

    Args:
        payload (CalendarActivity): Payload containing calendar activity data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CalendarController): Controller handling calendar activity operations.

    Returns:
        dict: Created calendar activity ID and creation timestamp.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update",
    summary="Update an existing calendar activity",
    response_description="Returns the updated calendar activity",
)
@inject
async def update(
    payload: CalendarActivity,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    """Update an existing calendar activity.

    Args:
        payload (CalendarActivity): Payload containing updated calendar activity data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CalendarController): Controller handling calendar activity operations.

    Returns:
        dict: Updated calendar activity ID and timestamp.
    """
    return await controller.update(payload)


@router.delete(
    "/{calendar_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a calendar activity",
    response_description="Returns the deleted calendar activity ID",
)
@inject
async def delete(
    calendar_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: CalendarController = Depends(Provide[Container.calendar_controller]),
):
    """Delete a calendar activity from the system by its ID.

    Args:
        calendar_id (int): ID of the calendar activity to delete.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (CalendarController): Controller handling calendar activity operations.

    Returns:
        dict: Deleted calendar activity ID and deletion timestamp.
    """
    return await controller.delete(calendar_id)
