"""add ondelete behavior to task model

Revision ID: 7e050834af80
Revises: a2e15722d231
Create Date: 2026-10-20 13:22:22.966461

"""

from collections.abc import Sequence

from alembic import op

# Revision identifiers.
revision: str = "7e050834af80"
down_revision: str | Sequence[str] | None = "a2e15722d231"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply ON DELETE behavior to task foreign keys."""

    # Drop existing foreign keys.
    op.drop_constraint(
        op.f("tasks_assigned_to_id_fkey"),
        "tasks",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("tasks_created_by_id_fkey"),
        "tasks",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("tasks_project_id_fkey"),
        "tasks",
        type_="foreignkey",
    )

    # Recreate them with explicit names and deletion behavior.
    op.create_foreign_key(
        op.f("tasks_assigned_to_id_fkey"),
        "tasks",
        "users",
        ["assigned_to_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        op.f("tasks_created_by_id_fkey"),
        "tasks",
        "users",
        ["created_by_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        op.f("tasks_project_id_fkey"),
        "tasks",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Restore the original foreign key behavior."""

    # Drop foreign keys with ON DELETE behavior.
    op.drop_constraint(
        op.f("tasks_assigned_to_id_fkey"),
        "tasks",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("tasks_created_by_id_fkey"),
        "tasks",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("tasks_project_id_fkey"),
        "tasks",
        type_="foreignkey",
    )

    # Restore original foreign keys without ON DELETE behavior.
    op.create_foreign_key(
        op.f("tasks_assigned_to_id_fkey"),
        "tasks",
        "users",
        ["assigned_to_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("tasks_created_by_id_fkey"),
        "tasks",
        "users",
        ["created_by_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("tasks_project_id_fkey"),
        "tasks",
        "projects",
        ["project_id"],
        ["id"],
    )
