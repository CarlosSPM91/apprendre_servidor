"""
Users DTO Object.

Data Transfer Object for user creation. Defines the fields required
to register or persist a new user.

:author: Carlos S. Paredes Morillo
"""

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    """DTO for creating a new user.

    Attributes:
        email (str): User's email address.
        name (str): User's first name.
        lastname (str): User's last name.
        dni (str): National identification number.
        pwd (str): User's password (raw, should be hashed before storage).
        phone (int): User's phone number.
        role (str): Role name assigned to the user.

    :author: Carlos S. Paredes Morillo
    """
    email: str
    name: str
    lastname: str
    dni:str
    pwd: str
    phone: int
    role: str
