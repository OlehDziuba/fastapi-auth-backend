import abc

from uuid import UUID

from auth_backend.core import User


class UsersRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, user: User) -> None:
        raise NotImplementedError
