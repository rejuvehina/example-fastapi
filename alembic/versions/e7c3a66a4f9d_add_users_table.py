"""add users table

Revision ID: e7c3a66a4f9d
Revises: 629ca9de0c71
Create Date: 2024-10-23 13:45:36.627251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7c3a66a4f9d'
down_revision: Union[str, None] = '629ca9de0c71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable= False), 
                    sa.Column("email", sa.String(), nullable= False),
                    sa.Column("password", sa.String(), nullable= False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone= True), server_default= sa.text("now()"), nullable= False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
