"""
JWT Payload.

Represents the content of the JWT used for authentication and authorization.

:author: Carlos S. Paredes Morillo
"""


class JwtPayload:
    def __init__(
        self, user_id: int, username: str, name: str, last_name: str, role: int
    ):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.role = role

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "JwtPayload":
        return cls(
            user_id= int(data.get("user_id")),
            username=data.get("username"),
            name=data.get("name"),
            last_name=data.get("last_name"),
            role=int(data.get("role")),
        )
