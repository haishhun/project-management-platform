from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import Boolean, DateTime, String, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.project_member import ProjectMember
    from app.models.task import Task


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    project_memberships: Mapped[list["ProjectMember"]] = relationship(
        back_populates="user",
    )

    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="created_by",
        foreign_keys="Task.created_by_id",
    )

    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assigned_to",
        foreign_keys="Task.assigned_to_id",
    )
