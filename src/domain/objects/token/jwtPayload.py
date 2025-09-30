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
    id: str
    username: str
    name: str
    last_name: str
    role: int
