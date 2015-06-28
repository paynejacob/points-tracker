"""empty message

Revision ID: 4e4bd2f0e8a4
Revises: c4019e037a7
Create Date: 2015-06-24 21:23:26.593406

"""

# revision identifiers, used by Alembic.
revision = '4e4bd2f0e8a4'
down_revision = 'c4019e037a7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('audio', 'filename', type_=sa.String(37), existing_type=sa.String(length=32), nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('audio', 'filename', type_=sa.String(32), existing_type=sa.String(length=37), nullable=True)
    ### end Alembic commands ###
