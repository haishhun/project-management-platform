from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ResourceDoesNotExistException, EmailAlreadyExistsException
from app.services.user import UserService


def test_create_and_get_by_id(session):
    service = UserService(session)
    user = service.register(
        email="a@test.com", password="password", first_name="Test1", last_name="Test2"
    )
    assert service.get_by_id(user.id).email == "a@test.com"

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
            first_name="Test1", last_name="Test2", email="a@test.com", password="password"
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
