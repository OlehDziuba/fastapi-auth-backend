from auth_backend.core import User
from .abc import UsersRepository, PasswordHasher
from .common import AuthData


class UserRegistrationInput(AuthData):
    first_name: str
    last_name: str

    def to_user(self) -> User:
        return User(**self.model_dump())


class UserRegistrateInteractor:
    def __init__(self, repository: UsersRepository, password_hasher: PasswordHasher):
        self._repository = repository
        self._password_hasher = password_hasher

    async def __call__(self, registration_input: UserRegistrationInput) -> User:
        registration_input.hash(self._password_hasher)
        user = registration_input.to_user()

        await self._repository.create(user)

        return user
