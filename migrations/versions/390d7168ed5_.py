"""empty message

Revision ID: 390d7168ed5
Revises: aa8faaf90e
Create Date: 2016-01-06 20:16:04.998405

"""

# revision identifiers, used by Alembic.
revision = '390d7168ed5'
down_revision = 'aa8faaf90e'

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
