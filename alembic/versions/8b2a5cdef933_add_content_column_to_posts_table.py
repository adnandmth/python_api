"""add content column to posts table

Revision ID: 8b2a5cdef933
Revises: 37bdbd4fcf96
Create Date: 2023-11-26 12:22:21.361522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b2a5cdef933'
down_revision: Union[str, None] = '37bdbd4fcf96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "content", sa.String(), nullable=False
        )
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
