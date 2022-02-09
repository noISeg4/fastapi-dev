"""add rest of the columns to posts

Revision ID: f27b02e9f523
Revises: 40a460e2c6f4
Create Date: 2022-02-08 23:03:01.507595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f27b02e9f523'
down_revision = '40a460e2c6f4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable= False, server_default= 'True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default= sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
