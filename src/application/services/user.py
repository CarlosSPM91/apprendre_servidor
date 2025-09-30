"""
Users Service.

Contains the business logic for user management, acting as the
application service layer.

:author: Carlos S. Paredes Morillo
"""
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.repositories.user import UserRepository


class UserService:
    """Application service for user operations.

    Coordinates between the repository and higher-level controllers.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, repo: UserRepository):
        """Initialize the service with a UserRepository.

        Args:
            repo (UserRepository): Repository handling persistence.

        :author: Carlos S. Paredes Morillo
        """
        self.userRepo = repo

    def create(self, payload: UserCreateDTO) -> UserDTO:
        """Create a new user.

        Args:
            payload (UserCreateDTO): Data for creating the user.

        Returns:
            UserDTO: Data Transfer Object representing the created user.

        :author: Carlos S. Paredes Morillo
        """
        self.userRepo.create(payload)