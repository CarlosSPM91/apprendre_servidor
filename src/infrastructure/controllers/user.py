"""
Users Controller.

Provides the controller layer between FastAPI endpoints and the application
services for user-related operations.

:author: Carlos S. Paredes Morillo
"""

from typing import List
from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.user.create_user_case import CreateUserCase
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.exceptions.except_manager import manage_user_except
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO



class UserController:
    """Controller for user operations.

    Acts as a bridge between the API layer and the application services.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(
        self,
        find_case: FindUserCase,
        create_case: CreateUserCase,
        update_case: UpdateUserCase,
        delete_case: DeleteUserCase,
    ):
        self.find_user_case = find_case
        self.create_user_case = create_case
        self.update_user_case = update_case
        self.delete_user_case = delete_case

    async def create_user(self, payload: UserCreateDTO):
        try:
            resp = await self.create_user_case.create(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)
        
    async def update_user(self, payload: UserUpdateDTO):
        try:
            await self.find_user_case.get_user_by_id(payload.user_id)
            resp = await self.update_user_case.update_user(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def change_password(self, payload:ChangePasswordDTO):
        try:
            await self.find_user_case.get_user_by_id(payload.user_id)
            resp = await self.update_user_case.change_password(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_all(self):
        try:
            resp: List[UserDTO] = await self.find_user_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_user(self, user_id: str):
        try:
            return await self.find_user_case.get_user_by_id(user_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def me(self, user_id: str):
        try:
            return await self.find_user_case.get_user_by_id(user_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def delete_user(self, user_id: int, user_eraser_id:int):
        try:
            await self.find_user_case.get_user_by_id(user_id)
            resp = await self.delete_user_case.delete(user_id, user_who_delete=user_eraser_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)
