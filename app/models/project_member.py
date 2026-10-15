from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    __table_args__ = (
        CheckConstraint(
            "role IN ('owner', 'member')",
            name="ck_project_members_role",
        ),
        Index("ix_project_members_user_id", "user_id"),
    )

    project_id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'member'"),
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
