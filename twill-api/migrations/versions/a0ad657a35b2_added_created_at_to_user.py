"""added created_at to user

Revision ID: a0ad657a35b2
Revises: 
Create Date: 2022-08-08 13:40:50.217477

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'a0ad657a35b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userdb')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userdb',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('twitter_handle', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('twitter_user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('twitter_followers_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('twitter_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('twitter_suspended', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('profile_image_url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userdb_pkey')
    )
    # ### end Alembic commands ###