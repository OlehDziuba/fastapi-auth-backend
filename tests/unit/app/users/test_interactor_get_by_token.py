import pytest

from unittest.mock import Mock

from faker import Faker

from auth_backend.app import (
    GetUserByTokenInteractor,
    UsersRepository,
    UserTokenHandler,
    UserTokenPayload,
    InvalidTokenError,
    UserEmailDoesNotExistError,
)
from auth_backend.core import User


@pytest.fixture
def user(faker: Faker) -> User:
    return User(
        email=faker.email(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name()
    )


@pytest.fixture
def users_repository_mock(user: User) -> Mock:
    mock = Mock(spec=UsersRepository, )

    mock.get_by_email.return_value = user

    return mock


@pytest.fixture
def token_handler_mock(user: User) -> Mock:
    mock = Mock(spec=UserTokenHandler, )

    mock.decode.return_value = UserTokenPayload(email=user.email)

    return mock


@pytest.fixture
def get_by_token_interactor(
        users_repository_mock: Mock,
        token_handler_mock: Mock,
) -> GetUserByTokenInteractor:
    return GetUserByTokenInteractor(users_repository_mock, token_handler_mock)


@pytest.mark.asyncio
async def test_invalid_token(get_by_token_interactor: GetUserByTokenInteractor, token_handler_mock: Mock) -> None:
    token_handler_mock.decode.side_effect = InvalidTokenError

    with pytest.raises(InvalidTokenError):
        await get_by_token_interactor("token")


@pytest.mark.asyncio
async def test_user_does_not_exist(
        get_by_token_interactor: GetUserByTokenInteractor,
        users_repository_mock: Mock
) -> None:
    users_repository_mock.get_by_email.return_value = None

    with pytest.raises(UserEmailDoesNotExistError):
        await get_by_token_interactor("token")


@pytest.mark.asyncio
async def test_valid_token(get_by_token_interactor: GetUserByTokenInteractor, user: User):
    user_by_token = await get_by_token_interactor("token")

    assert user_by_token == user
