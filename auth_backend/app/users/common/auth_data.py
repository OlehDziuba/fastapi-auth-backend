import pydantic

from auth_backend.app.users.abc import PasswordHasher


class AuthData(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str

    def hash(self, hasher: PasswordHasher) -> None:
        self.password = hasher.hash(self.password)

    @pydantic.field_validator("email")
    @classmethod
    def _normalize_email(cls, email: str) -> str:
        return email.lower().strip()
