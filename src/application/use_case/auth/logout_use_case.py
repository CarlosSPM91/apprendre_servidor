"""
Logout Use Case.

Handles user logout operations by invalidating JWT tokens.

:author: Carlos S. Paredes Morillo
"""

from src.application.services.token_service import TokenService


class LogoutUseCase:
    """Use case for handling user logout."""

    def __init__(self, token_service: TokenService):
        """
        Initialize the LogoutUseCase with the required token service.

        Args:
            token_service (TokenService): Service for managing JWT tokens.
        """
        self.token_service = token_service

    async def logout(self, user_id: int) -> bool:
        """
        Invalidate the user's JWT token, effectively logging them out.

        Args:
            user_id (int): The ID of the user to log out.

        Returns:
            bool: True if the token was successfully invalidated.
        """
        return await self.token_service.invalidate_token(user_id)
