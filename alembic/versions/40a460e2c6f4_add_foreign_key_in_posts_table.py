"""add foreign key in posts table

Revision ID: 40a460e2c6f4
Revises: 82de3d7a34c4
Create Date: 2022-02-08 22:56:09.048709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40a460e2c6f4'
down_revision = '82de3d7a34c4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('posts_users_fkey', 
                           source_table= 'posts', 
                           referent_table= 'users', 
                           local_cols= ['owner_id'], 
                           remote_cols= ['id'],
                           ondelete= "CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
    pass
