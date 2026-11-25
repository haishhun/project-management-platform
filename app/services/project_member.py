from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    ResourceDoesNotExistException,
)
from app.models.project_member import ProjectMember, ProjectRole
from app.repositories import ProjectMemberRepository, ProjectRepository, UserRepository


class ProjectMemberService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)
        self.user_repo = UserRepository(db)

    def add_member(
        self,
        project_id: UUID,
        actor_id: UUID,
        user_id: UUID,
    ) -> ProjectMember:
        try:
            project = self.project_repo.get_by_id(project_id=project_id)
            if project is None:
                raise ResourceDoesNotExistException("Project does not exist.")
            project_membership = self.project_member_repo.get_by_project_and_member(
                project_id=project_id, user_id=actor_id
            )

            if project_membership is None:
                raise ForbiddenException("Access Forbidden.")
            if project_membership.role != ProjectRole.OWNER:
                raise ForbiddenException(
                    "You do not have permission to add members to the project."
                )

            user = self.user_repo.get_by_id(user_id=user_id)
            if user is None:
                raise ResourceDoesNotExistException("User does not exist.")

            existing_membership = self.project_member_repo.get_by_project_and_member(
                project_id=project_id,
                user_id=user_id,
            )
            if existing_membership is not None:
                raise ConflictException("User is already a project member.")
            membership = self.project_member_repo.create(
                project_id=project_id, user_id=user_id, role=ProjectRole.MEMBER
            )
            self.db.commit()
            return membership
        except IntegrityError:
            self.db.rollback()
            raise ConflictException("User is already a project member.")
        except Exception:
            self.db.rollback()
            raise

    def remove_member(
        self,
        project_id: UUID,
        actor_id: UUID,
        user_id: UUID,
    ) -> None:
        try:
            project = self.project_repo.get_by_id(project_id=project_id)
            if project is None:
                raise ResourceDoesNotExistException("Project does not exist.")

            actor_membership = self.project_member_repo.get_by_project_and_member(
                project_id=project_id, user_id=actor_id
            )
            if actor_membership is None:
                raise ResourceDoesNotExistException("Project does not exist.")
            if actor_membership.role != ProjectRole.OWNER:
                raise ForbiddenException(
                    "You do not have permission to remove members of the project."
                )

            target_membership = self.project_member_repo.get_by_project_and_member(
                project_id=project_id,
                user_id=user_id,
            )
            if target_membership is None:
                raise ResourceDoesNotExistException(
                    "User is not associated with this project."
                )
            if target_membership.role == ProjectRole.OWNER:
                raise ForbiddenException("The project owner cannot be removed.")
            self.project_member_repo.delete(project_id=project_id, user_id=user_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
