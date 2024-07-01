from auth_backend.core import User

from .abc import UsersRepository, UserTokenHandler, UserTokenPayload, PasswordHasher
from .common import AuthData
from .exceptions import UserEmailDoesNotExistError, PasswordDoesNotMatchError


class UserLoginInteractor:
    def __init__(self, repository: UsersRepository, password_hasher: PasswordHasher, token_handler: UserTokenHandler):
        self._repository = repository
        self._password_hasher = password_hasher
        self._token_handler = token_handler

    async def __call__(self, auth_data: AuthData) -> str:
        auth_data.hash(self._password_hasher)

        user = await self._get_user(auth_data)
        token = self._generate_token(user)

        return "Bearer " + token

    async def _get_user(self, auth_data: AuthData) -> User:
        user = await self._repository.get_by_email(auth_data.email)
        if not user:
            raise UserEmailDoesNotExistError()
        if auth_data.password != user.password:
            raise PasswordDoesNotMatchError()

        return user

    def _generate_token(self, user: User) -> str:
        token_payload = UserTokenPayload.from_user(user)
        token = self._token_handler.generate(token_payload)

        return token
