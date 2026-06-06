"""Add RFLP traceability FKs: requirement_id to functions, function_id to scs

Revision ID: 002
Revises: 001
Create Date: 2026-05-03
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("functions", sa.Column("requirement_id", UUID(as_uuid=True), sa.ForeignKey("requirements.id"), nullable=True))
    op.add_column("scs", sa.Column("function_id", UUID(as_uuid=True), sa.ForeignKey("functions.id"), nullable=True))


def downgrade() -> None:
    op.drop_column("scs", "function_id")
    op.drop_column("functions", "requirement_id")
