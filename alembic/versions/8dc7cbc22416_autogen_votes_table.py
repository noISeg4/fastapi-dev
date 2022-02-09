"""AutoGen votes table

Revision ID: 8dc7cbc22416
Revises: f27b02e9f523
Create Date: 2022-02-08 23:14:04.525832

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8dc7cbc22416'
down_revision = 'f27b02e9f523'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # op.drop_table('00_votes')
    # op.drop_table('00_posts')
    # op.drop_table('00_products')
    # op.drop_table('00_users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('00_users',
    #                 sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    #                 sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    #                 sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    #                 sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    #                 sa.PrimaryKeyConstraint('id', name='users_pkey'),
    #                 sa.UniqueConstraint('email', name='users_email_key'),
    #                 postgresql_ignore_search_path=False
    # )
    # op.create_table('00_products',
    #                 sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    #                 sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    #                 sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    #                 sa.Column('on_sale', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    #                 sa.Column('inventory', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    #                 sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    #                 sa.PrimaryKeyConstraint('id', name='products_pkey')
    # )
    # op.create_table('00_posts',
    #                 sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('posts_id_seq1'::regclass)"), autoincrement=True, nullable=False),
    #                 sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    #                 sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    #                 sa.Column('published', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    #                 sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    #                 sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    #                 sa.ForeignKeyConstraint(['owner_id'], ['00_users.id'], name='posts_owner_id_fkey', ondelete='CASCADE'),
    #                 sa.PrimaryKeyConstraint('id', name='posts_pkey1'),
    #                 postgresql_ignore_search_path=False
    # )
    # op.create_table('00_votes',
    #                 sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    #                 sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    #                 sa.ForeignKeyConstraint(['post_id'], ['00_posts.id'], name='votes_post_id_fkey', ondelete='CASCADE'),
    #                 sa.ForeignKeyConstraint(['user_id'], ['00_users.id'], name='votes_user_id_fkey', ondelete='CASCADE'),
    #                 sa.PrimaryKeyConstraint('user_id', 'post_id', name='votes_pkey')
    )
    op.drop_table('votes')
    # ### end Alembic commands ###
