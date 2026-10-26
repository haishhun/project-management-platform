from uuid import UUID

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
