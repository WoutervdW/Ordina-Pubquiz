"""removed test table images

Revision ID: aaae76ff57f5
Revises: 437a64b193ff
Create Date: 2019-12-04 08:20:13.345103

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aaae76ff57f5'
down_revision = '437a64b193ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('img_filename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('img_data', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    # ### end Alembic commands ###
