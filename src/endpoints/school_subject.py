from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.school_subject import SchoolSubjectController
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/school-subjects", tags=["school-subject"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all school subject",
    response_description="Returns a list of all school subject",
)
@inject
async def find_all(
    controller: SchoolSubjectController = Depends(Provide[Container.school_subject_controller]),
):
    return await controller.get_all()


@router.get(
    "/{school_subject_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of school subject",
    response_description="Returns the information of a school subject",
)
@inject
async def find(
    school_subject_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SchoolSubjectController = Depends(Provide[Container.school_subject_controller]),
):
    return await controller.get(school_subject_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a school subject",
    response_description="Returns the information of a school subject",
)
@inject
async def create(
    payload: SchoolSubject,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SchoolSubjectController = Depends(Provide[Container.school_subject_controller]),
):
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update",
    summary="Update an existing school subject",
    response_description="Returns the updated school subject",
)
@inject
async def update(
    payload: SchoolSubject,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SchoolSubjectController = Depends(Provide[Container.school_subject_controller]),
):
    return await controller.update(payload)


@router.delete(
    "/{school_subject_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a school subject",
    response_description="Returns the deleted school subject id",
)
@inject
async def delete(
    school_subject_id: int,
    controller: SchoolSubjectController = Depends(Provide[Container.school_subject_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(school_subject_id)
