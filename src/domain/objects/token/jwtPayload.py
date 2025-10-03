"""
JWT Payload.

Represents the content of the JWT used for authentication and authorization.

:author: Carlos S. Paredes Morillo
"""
class JwtPayload:
    """Data stored inside a JWT token.

    Attributes:
        id (str): User ID.
        username (str): Username.
        name (str): User's first name.
        last_name (str): User's last name.
        role (int): Role identifier.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, user_id: int, username: str, name: str, last_name: str, role: int):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.role = role