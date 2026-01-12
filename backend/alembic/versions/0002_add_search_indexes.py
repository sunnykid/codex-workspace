"""add search indexes

Revision ID: 0002_add_search_indexes
Revises: 0001_init_models
Create Date: 2025-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0002_add_search_indexes"
down_revision = "0001_init_models"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "files",
        "tags",
        type_=postgresql.JSONB(),
        postgresql_using="tags::jsonb",
    )
    op.create_index(
        "ix_files_owner_created_at",
        "files",
        ["owner_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_files_tags_gin",
        "files",
        ["tags"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_files_tags_gin", table_name="files")
    op.drop_index("ix_files_owner_created_at", table_name="files")
    op.alter_column(
        "files",
        "tags",
        type_=sa.JSON(),
        postgresql_using="tags::json",
    )
