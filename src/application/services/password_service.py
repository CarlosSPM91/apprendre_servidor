import hashlib


class PasswordService:
    """Service for password hashing."""

    def __init__(self):
        """Initialize the PasswordService."""
        pass

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password using SHA-256.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The SHA-256 hashed password as a hexadecimal string.
        """
        return hashlib.sha256(password.encode()).hexdigest()
