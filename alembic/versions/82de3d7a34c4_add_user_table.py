"""add user table

Revision ID: 82de3d7a34c4
Revises: 36aab669b1b2
Create Date: 2022-02-08 22:43:11.449590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82de3d7a34c4'
down_revision = '36aab669b1b2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default= sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
