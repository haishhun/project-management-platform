from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

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

