import abc

import pydantic

from typing import Self

from auth_backend.core import User


class UserTokenPayload(pydantic.BaseModel):
    email: str

    @classmethod
    def from_user(cls: Self, user: User) -> Self:
        return cls.model_validate({"email": user.email})


class InvalidTokenError(Exception):
    pass


class UserTokenHandler(abc.ABC):
    @abc.abstractmethod
    def generate(self, payload: UserTokenPayload) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, token: str) -> UserTokenPayload:
        raise NotImplementedError
