
import hashlib


class PasswordService:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
