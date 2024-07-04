import pytest

from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import UUID

from faker import Faker

from auth_backend.app import (
    EmailAlreadyExistsError,
    UsersRepository,
    UserRegistrationInput,
    UserRegistrateInteractor,
    PasswordHasher,
    UserTokenHandler,
)
from auth_backend.core import User


@pytest.fixture
def registration_input(faker: Faker) -> UserRegistrationInput:
    return UserRegistrationInput(
        email=faker.email(),
        password=faker.password(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )


@pytest.fixture
def password_hasher_mock() -> Mock:
    mock = Mock(spec=PasswordHasher, )

    mock.hash.side_effect = lambda x: x + "_hashed"

    return mock


@pytest.fixture
def users_repository_mock(user: User) -> Mock:
    mock = Mock(spec=UsersRepository, )

    mock.get_by_email.return_value = None
    mock.create.side_effect = lambda x: x

    return mock


@pytest.fixture
def user(registration_input: UserRegistrationInput, password_hasher_mock: Mock) -> User:
    return User(
        email=registration_input.email,
        password=password_hasher_mock.hash(registration_input.password),
        first_name=registration_input.first_name,
        last_name=registration_input.last_name
    )


@pytest.fixture
def registrate_interactor(
        users_repository_mock: Mock,
        password_hasher_mock: Mock
) -> UserRegistrateInteractor:
    return UserRegistrateInteractor(users_repository_mock, password_hasher_mock)


@pytest.mark.asyncio
async def test_email_already_exists(
        registration_input: UserRegistrationInput,
        user: User,
        registrate_interactor: UserRegistrateInteractor,
        users_repository_mock: Mock
):
    users_repository_mock.get_by_email.return_value = user

    with pytest.raises(EmailAlreadyExistsError):
        await registrate_interactor(registration_input)


@pytest.mark.asyncio
async def test_created_user_fields(
        registration_input: UserRegistrationInput,
        user: User,
        registrate_interactor: UserRegistrateInteractor,
        users_repository_mock: Mock,
        password_hasher_mock: Mock,
):
    initial_password = registration_input.password

    returned_user = await registrate_interactor(registration_input)

    utc_now = datetime.utcnow()
    created_user = users_repository_mock.create.mock_calls[0].args[0]

    assert returned_user == created_user
    assert isinstance(created_user.id, UUID)
    assert created_user.email == registration_input.email
    assert created_user.password == password_hasher_mock.hash(initial_password)
    assert created_user.first_name == registration_input.first_name
    assert created_user.last_name == registration_input.last_name
    assert (utc_now - timedelta(seconds=1)) <= created_user.created_at <= utc_now
    assert (utc_now - timedelta(seconds=1)) <= created_user.updated_at <= utc_now
    assert (utc_now - timedelta(seconds=1)) <= created_user.last_login_at <= utc_now
