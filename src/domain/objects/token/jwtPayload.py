"""
JWT Payload.

Represents the content of the JWT used for authentication and authorization.

:author: Carlos S. Paredes Morillo
"""


from datetime import datetime, timedelta, timezone


class JwtPayload:
    def __init__(
        self, user_id: int, username: str, name: str, last_name: str, role: int, iat:datetime = None, exp:datetime = None
    ):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.last_name = last_name
        self.role = role
        self.iat= iat or datetime.now(timezone.utc)
        self.exp= exp or datetime.now(timezone.utc) + timedelta(hours=24)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "role": self.role,
            "iat": self.iat,
            "exp": self.exp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "JwtPayload":
        return cls(
            user_id= int(data.get("user_id")),
            username=data.get("username"),
            name=data.get("name"),
            last_name=data.get("last_name"),
            role=int(data.get("role")),
            iat=datetime.fromtimestamp(data.get("iat"), tz=timezone.utc),
            exp=datetime.fromtimestamp(data.get("exp"), tz=timezone.utc)
        )
