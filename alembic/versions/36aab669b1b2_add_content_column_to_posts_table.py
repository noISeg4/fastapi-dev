"""add content column to posts table

Revision ID: 36aab669b1b2
Revises: f2886efde2b1
Create Date: 2022-02-08 22:37:40.600959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36aab669b1b2'
down_revision = 'f2886efde2b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
