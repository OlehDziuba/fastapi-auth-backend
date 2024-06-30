import pydantic

from datetime import datetime
from typing import Self
from uuid import UUID

from auth_backend.core import User


class UserResponse(pydantic.BaseModel):
    id: UUID
    email: pydantic.EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime

    @classmethod
    def from_user(cls: Self, user: User) -> Self:
        return cls.model_validate(user.model_dump())
