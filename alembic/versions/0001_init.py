"""init schema

Revision ID: 0001_init
Revises:
Create Date: 2026-04-26
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("short_code", sa.String(length=20), nullable=False, unique=True),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_links_short_code", "links", ["short_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_links_short_code", table_name="links")
    op.drop_table("links")
