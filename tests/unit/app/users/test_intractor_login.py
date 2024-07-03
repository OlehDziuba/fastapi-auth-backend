import pytest

from datetime import datetime, timedelta
from unittest.mock import Mock

from faker import Faker

from auth_backend.app import (
    AuthData,
    UserTokenHandler,
    UserLoginInteractor,
    UsersRepository,
    UserEmailDoesNotExistError,
    PasswordDoesNotMatchError, PasswordHasher
)
from auth_backend.core import User


@pytest.fixture
def auth_data(faker: Faker) -> AuthData:
    return AuthData(email=faker.email(), password=faker.password())


@pytest.fixture
def user(auth_data: AuthData, faker: Faker,) -> User:
    return User(
        email=auth_data.email,
        password=auth_data.password + "_hashed",
        first_name=faker.first_name(),
        last_name=faker.last_name()
    )


@pytest.fixture
def users_repository_mock(user: User) -> Mock:
    mock = Mock(spec=UsersRepository, )

    mock.get_by_email.return_value = user

    return mock


@pytest.fixture
def password_hasher_mock(user: User) -> Mock:
    mock = Mock(spec=PasswordHasher, )

    mock.hash.side_effect = lambda x: x + "_hashed"

    return mock


@pytest.fixture
def token_handler_mock(user: User) -> Mock:
    mock = Mock(spec=UserTokenHandler, )

    mock.generate.return_value = user.email

    return mock


@pytest.fixture
def login_interactor(
        users_repository_mock: Mock,
        token_handler_mock: Mock,
        password_hasher_mock: Mock
) -> UserLoginInteractor:
    return UserLoginInteractor(users_repository_mock, password_hasher_mock, token_handler_mock)


@pytest.mark.asyncio
async def test_email_does_not_exists(
        auth_data: AuthData,
        login_interactor: UserLoginInteractor,
        users_repository_mock: Mock
):
    users_repository_mock.get_by_email.return_value = None

    with pytest.raises(UserEmailDoesNotExistError):
        await login_interactor(auth_data)


@pytest.mark.asyncio
async def test_invalid_password(auth_data: AuthData, login_interactor: UserLoginInteractor):
    auth_data.password = "invalid_password"

    with pytest.raises(PasswordDoesNotMatchError):
        await login_interactor(auth_data)


@pytest.mark.asyncio
async def test_valid_token_with_added_prefix(auth_data: AuthData, user: User, login_interactor: UserLoginInteractor):
    token = await login_interactor(auth_data)

    assert token == f"Bearer {user.email}"


@pytest.mark.asyncio
async def test_auth_data_was_hashed(
        auth_data: AuthData,
        user: User,
        login_interactor: UserLoginInteractor,
        password_hasher_mock: Mock
):
    password_hasher_mock.hash.side_effect = lambda x: x

    with pytest.raises(PasswordDoesNotMatchError):
        await login_interactor(auth_data)


@pytest.mark.asyncio
async def test_last_login_at_was_updated(
        auth_data: AuthData,
        user: User,
        login_interactor: UserLoginInteractor,
        users_repository_mock: Mock
):
    await login_interactor(auth_data)

    utc_now = datetime.utcnow()
    called_for_user = users_repository_mock.update.mock_calls[0].args[0]

    assert len(users_repository_mock.update.mock_calls) == 1
    assert called_for_user.id == user.id
    assert (utc_now - timedelta(seconds=1)) < called_for_user.last_login_at <= utc_now
