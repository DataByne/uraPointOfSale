"""empty message

Revision ID: 49580a68ff63
Revises: 1bab4c378730
Create Date: 2019-11-10 11:57:16.241464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49580a68ff63'
down_revision = '1bab4c378730'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('country', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'country')
    # ### end Alembic commands ###