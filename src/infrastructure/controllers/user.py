"""
Users Controller.

Provides the controller layer between FastAPI endpoints and the application
services for user-related operations.

:author: Carlos S. Paredes Morillo
"""
from src.application.services.user import UserService
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO


class UserController:
    """Controller for user operations.

    Acts as a bridge between the API layer and the application services.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, service: UserService):
        """Initialize the controller with a UserService.

        Args:
            service (UserService): Service providing user-related business logic.

        :author: Carlos S. Paredes Morillo
        """
        self.userService = service
        
    async def create_user(self, payload: UserCreateDTO) -> UserDTO:
        """Create a new user.

        Args:
            payload (UserCreateDTO): Data for creating the user.

        Returns:
            UserDTO: Data Transfer Object representing the created user.

        :author: Carlos S. Paredes Morillo
        """
        return await self.userService.create(payload)