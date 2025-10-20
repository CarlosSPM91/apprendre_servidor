
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.parent import ParentController
from src.infrastructure.entities.users.parents import Parent
from src.middleware.token.authenticateToken import get_current_user, require_role

router = APIRouter(prefix="/parent", tags=["parent"])

@router.get(
    "/{user_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of the parent",
    response_description="Returns the information of the parent",
)
@inject
async def find(
    user_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    return await controller.get_parent(user_id=user_id)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create the parent",
    response_description="Returns the information of parent",
)
@inject
async def create(
    payload: Parent,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    return await controller.create(payload)

@router.delete(
    "/{user_id}/{student_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete the parent",
    response_description="Returns the information of deleted parent",
)
@inject
async def delete(
    user_id: int,
    student_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    return await controller.delete(user_id=user_id, student_id=student_id)