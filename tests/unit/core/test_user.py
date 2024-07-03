import pydantic
import pytest

from datetime import datetime, timedelta
from uuid import UUID

from faker import Faker

from auth_backend.core import User


@pytest.fixture
def user_data_without_default_fields(faker: Faker) -> dict:
    return {
        "email": faker.email(),
        "password": faker.password(),
        "first_name":faker.first_name(),
        "last_name": faker.last_name(),
    }


@pytest.fixture
def user_data_with_default_fields(faker: Faker, user_data_without_default_fields: dict) -> dict:
    user_data_without_default_fields.update({
        "id": UUID(faker.uuid4()),
        "created_at": faker.date_time(),
        "updated_at": faker.date_time(),
        "last_login_at": faker.date_time(),
    })

    return user_data_without_default_fields


def test_create_without_default_fields(user_data_without_default_fields: dict):
    user = User(**user_data_without_default_fields)
    utc_now = datetime.utcnow()

    assert isinstance(user.id, UUID)
    assert user.email == user_data_without_default_fields["email"]
    assert user.password == user_data_without_default_fields["password"]
    assert user.first_name == user_data_without_default_fields["first_name"]
    assert user.last_name == user_data_without_default_fields["last_name"]
    assert (utc_now - timedelta(seconds=2)) <= user.created_at <= utc_now
    assert (utc_now - timedelta(seconds=2)) <= user.updated_at <= utc_now
    assert (utc_now - timedelta(seconds=2)) <= user.last_login_at <= utc_now


def test_create_with_default_fields(user_data_with_default_fields: dict):
    user = User(**user_data_with_default_fields)

    assert user.id == user_data_with_default_fields["id"]
    assert user.created_at == user_data_with_default_fields["created_at"]
    assert user.updated_at == user_data_with_default_fields["updated_at"]
    assert user.last_login_at == user_data_with_default_fields["last_login_at"]


def test_email_was_normalized(user_data_without_default_fields: dict):
    user_data_without_default_fields["email"] = " " * 2 + user_data_without_default_fields["email"].upper() + " " * 3
    user = User(**user_data_without_default_fields)

    assert user.email == user_data_without_default_fields["email"].strip().lower()


def test_invalid_email(user_data_without_default_fields: dict):
    user_data_without_default_fields["email"] = "abc"

    with pytest.raises(pydantic.ValidationError):
        User(**user_data_without_default_fields)
