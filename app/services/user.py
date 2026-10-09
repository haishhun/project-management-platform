from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsException,
    ResourceDoesNotExistException,
)
from app.core.security import hash_password
from app.models import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> User:
        email = email.strip().lower()
        if self.users.get_by_email(email):
            raise EmailAlreadyExistsException("Email already in use.")

        password_hash = hash_password(password)
        try:
            user = self.users.create(email, password_hash, first_name, last_name)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise EmailAlreadyExistsException("Email already in use.")
        except Exception:
            self.db.rollback()
            raise
        return user

    def update(
        self,
        user_id: UUID,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> User:
        if email is not None:
            email = email.strip().lower()
        try:
            user = self.users.update(
                user_id=user_id, first_name=first_name, last_name=last_name, email=email
            )
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise EmailAlreadyExistsException("Email already in use.")
        except Exception:
            self.db.rollback()
            raise

        return user

    def delete(self, user_id: UUID) -> None:
        try:
            self.users.delete(user_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, user_id: UUID) -> User:
        user = self.users.get_by_id(user_id)
        if user is None:
            raise ResourceDoesNotExistException("User does not exist.")
        return user

    def get_by_email(self, email: str) -> User | None:
        email = email.strip().lower()
        return self.users.get_by_email(email)
