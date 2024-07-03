import pydantic
import pytest

from unittest.mock import Mock

from faker import Faker

from auth_backend.app import AuthData, PasswordHasher


@pytest.fixture
def auth_data_input(faker: Faker) -> dict:
    return {"email": faker.email(), "password": faker.password()}


@pytest.fixture
def hasher_mock() -> PasswordHasher:
    hasher_mock = Mock(spec=PasswordHasher)
    hasher_mock.hash.return_value = "hashed_password"

    return hasher_mock


def test_create(auth_data_input: dict):
    auth_data = AuthData(**auth_data_input)

    assert auth_data.email == auth_data_input["email"]
    assert auth_data.password == auth_data_input["password"]


def test_email_was_normalized(auth_data_input: dict):
    auth_data_input["email"] = (" " * 2) + auth_data_input["email"].upper() + (" " * 3)

    auth_data = AuthData(**auth_data_input)

    assert auth_data.email == auth_data_input["email"].strip().lower()


def test_invalid_email(auth_data_input: dict):
    auth_data_input["email"] = "abc"

    with pytest.raises(pydantic.ValidationError):
        AuthData(**auth_data_input)


def test_hash(auth_data_input: dict, hasher_mock: PasswordHasher):
    auth_data = AuthData(**auth_data_input)
    auth_data.hash(hasher_mock)

    assert auth_data.password == "hashed_password"
