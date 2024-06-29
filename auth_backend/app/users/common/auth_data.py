import pydantic

from auth_backend.app.users.abc import PasswordHasher


class AuthData(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str

    def hash(self, hasher: PasswordHasher) -> None:
        self.password = hasher.hash(self.password)
