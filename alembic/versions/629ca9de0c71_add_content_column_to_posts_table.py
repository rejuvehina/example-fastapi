"""add content column to posts table

Revision ID: 629ca9de0c71
Revises: c9bd04d9dd09
Create Date: 2024-10-23 13:27:34.625177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '629ca9de0c71'
down_revision: Union[str, None] = 'c9bd04d9dd09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
