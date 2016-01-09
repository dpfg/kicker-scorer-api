"""empty message

Revision ID: 188f9d0871a
Revises: 2ef83e4c423
Create Date: 2016-01-06 20:08:23.895408

"""

# revision identifiers, used by Alembic.
revision = '188f9d0871a'
down_revision = '2ef83e4c423'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match', sa.Column('completed', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('match', 'completed')
    ### end Alembic commands ###
