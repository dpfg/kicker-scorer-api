"""empty message

Revision ID: 81d730bb63
Revises: c51c40a0de
Create Date: 2016-01-04 22:30:39.729115

"""

# revision identifiers, used by Alembic.
revision = '81d730bb63'
down_revision = 'c51c40a0de'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match_goal', sa.Column('team_id', sa.Integer(), nullable=False))
    op.alter_column('match_goal', 'player_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('match_goal', 'player_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('match_goal', 'team_id')
    ### end Alembic commands ###
