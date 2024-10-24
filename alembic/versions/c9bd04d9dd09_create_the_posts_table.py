"""create the posts table

Revision ID: c9bd04d9dd09
Revises: 
Create Date: 2024-10-23 12:54:47.972014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9bd04d9dd09'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable= False, primary_key= True), sa.Column("title", sa.String(), nullable= False))
    pass

def downgrade() -> None:
    op.drop_table("posts")
    pass