from uuid import UUID

import pytest

from app.core.exceptions import (
    EmailAlreadyExistsException,
    ResourceDoesNotExistException,
)
from app.core.security import verify_password
from app.services.user import UserService


def test_create_and_get_by_id(session):
    service = UserService(session)
    user = service.register(
        email="a@test.com", password="password", first_name="Test1", last_name="Test2"
    )
    assert service.get_by_id(user.id).email == "a@test.com"


def test_create_and_check_email_normalization(session):
    service = UserService(session)
    user = service.register(
        email="         TeStEmaIl@test.com",
        password="password",
        first_name="Test1",
        last_name="Test2",
    )
    assert service.get_by_id(user.id).email == "testemail@test.com"


def test_create_and_check_password_hashing(session):
    service = UserService(session)
    user = service.register(
        email="a@test.com", password="password", first_name="Test1", last_name="Test2"
    )
    stored_password = service.get_by_id(user.id).password_hash
    assert stored_password != "password"
    assert stored_password.startswith("$argon2")
    assert verify_password("password", stored_password)
    assert not verify_password("wrong-password", stored_password)


def test_create_and_get_by_email(session):
    service = UserService(session)
    user = service.register(
        email="a@test.com", password="password", first_name="Test1", last_name="Test2"
    )
    assert service.get_by_email(user.email).first_name == "Test1"


def test_get_by_email_returns_none_when_missing(session):
    assert UserService(session).get_by_email("nope@test.com") is None


def test_create_duplicate_email_fails(session):
    service = UserService(session)
    service.register(
        first_name="Test1", last_name="Test2", email="a@test.com", password="password"
    )
    with pytest.raises(EmailAlreadyExistsException):
        service.register(
            first_name="Test1",
            last_name="Test2",
            email="a@test.com",
            password="password",
        )


def test_user_update(session):
    service = UserService(session)
    user = service.register(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password="password",
    )

    updated_user = service.update(
        user.id,
        first_name="Updated1",
        last_name="Updated2",
        email="updated@test.com",
    )

    assert updated_user.id == user.id
    assert updated_user.first_name == "Updated1"
    assert updated_user.last_name == "Updated2"
    assert updated_user.email == "updated@test.com"


def test_user_update_duplicate_email_fails(session):
    service = UserService(session)
    user_1 = service.register(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password="password",
    )

    user_2 = service.register(
        first_name="Test1",
        last_name="Test2",
        email="ab@test.com",
        password="password",
    )

    with pytest.raises(EmailAlreadyExistsException):
        service.update(
            user_2.id,
            first_name="Updated1",
            last_name="Updated2",
            email=user_1.email,
        )


def test_user_update_check_email_normalization(session):
    service = UserService(session)
    user = service.register(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password="password",
    )

    updated_user = service.update(
        user.id,
        first_name="Updated1",
        last_name="Updated2",
        email="     UpDaTeD@test.com   ",
    )

    assert updated_user.email == "updated@test.com"


def test_user_partial_update(session):
    service = UserService(session)
    user = service.register(
        first_name="Test1",
        last_name="Test2",
        email="a@test.com",
        password="password",
    )

    updated_user = service.update(
        user.id,
        first_name="Updated1",
    )

    assert updated_user.first_name == "Updated1"
    assert updated_user.last_name == "Test2"
    assert updated_user.email == "a@test.com"


def test_user_update_not_found(session):
    service = UserService(session)

    with pytest.raises(ResourceDoesNotExistException):
        service.update(
            UUID("579d2ad8-30a4-4bcd-b98a-484b1faa44e1"),
            first_name="Updated1",
        )


def test_user_delete(session):
    service = UserService(session)
    user = service.register(
        first_name="Test1", last_name="Test2", email="a@test.com", password="password"
    )
    service.delete(user.id)

    with pytest.raises(ResourceDoesNotExistException):
        service.get_by_id(user.id)


def test_user_delete_not_found(session):
    service = UserService(session)
    with pytest.raises(ResourceDoesNotExistException):
        service.delete(UUID("579d2ad8-30a4-4bcd-b98a-484b1faa44e1"))


def test_register_rolls_back_after_integrity_error(session):
    service = UserService(session)
    user1 = service.register(
        email="first@test.com",
        password="password123",
        first_name="First",
        last_name="User",
    )
    service.register(
        email="second@test.com",
        password="password123",
        first_name="Second",
        last_name="User",
    )

    with pytest.raises(EmailAlreadyExistsException):
        service.update(user1.id, email="second@test.com")

    retrieved_user = service.get_by_id(user1.id)
    assert retrieved_user.email == "first@test.com"

    new_user = service.register(
        email="third@test.com",
        password="password123",
        first_name="Third",
        last_name="User",
    )
    assert new_user.email == "third@test.com"
