from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceDoesNotExistException
from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, email: str, password_hash: str, first_name: str, last_name: str
    ) -> User:
        new_user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
        )
        self.db.add(new_user)
        self.db.flush()
        return new_user

    def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_by_email(self, user_email: str) -> User | None:
        query = select(User).where(User.email == user_email)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def update(
        self,
        user_id: UUID,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> User:
        user = self.get_by_id(user_id)
        if user is None:
            raise ResourceDoesNotExistException("User does not exist.")

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email

        self.db.commit()
        self.db.refresh(user)
        return user
