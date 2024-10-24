"""For Updating

Revision ID: d4440fc155e5
Revises: 8bc42e1f2032
Create Date: 2024-10-24 06:37:15.026762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4440fc155e5'
down_revision: Union[str, None] = '8bc42e1f2032'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable = False))
    op.create_foreign_key("posts_users_fk", source_table ="posts", referent_table ="users", local_cols= ["owner_id"], remote_cols= ["id"], ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name= "posts")
    op.drop_column("posts", "owner_id")
    pass