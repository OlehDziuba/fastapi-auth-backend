from .abc import UsersRepository, UserTokenHandler

from auth_backend.core import User
from .exceptions import UserEmailDoesNotExistError


class GetUserByTokenInteractor:
    def __init__(self, users_repository: UsersRepository, token_handler: UserTokenHandler):
        self._users_repository = users_repository
        self._token_handler = token_handler

    async def __call__(self, token: str) -> User:
        user_token_payload = await self._token_handler.decode(token)
        user = await self._users_repository.get_by_email(user_token_payload.email)

        return user

    async def _get_user(self, email: str) -> User:
        user = await self._users_repository.get_by_email(email)

        if not user:
            raise UserEmailDoesNotExistError

        return user
