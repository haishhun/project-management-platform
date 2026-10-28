from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProjectMember
from app.models.project_member import ProjectRole


class ProjectMemberRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        project_id: UUID,
        user_id: UUID,
        role: ProjectRole = ProjectRole.MEMBER,
    ) -> ProjectMember:
        new_member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
        self.db.add(new_member)
        self.db.flush()

        return new_member

    def get_by_project_and_member(
        self, project_id: UUID, user_id: UUID
    ) -> ProjectMember | None:
        query = select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_project_memberships(self, project_id: UUID) -> Sequence[ProjectMember]:
        query = (
            select(ProjectMember)
            .where(ProjectMember.project_id == project_id)
            .order_by(ProjectMember.joined_at)
        )
        result = self.db.execute(query)
        return result.scalars().all()
