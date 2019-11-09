"""empty message

Revision ID: a5c5694765b4
Revises: fc198dd9d725
Create Date: 2019-11-08 22:09:11.827722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5c5694765b4'
down_revision = 'fc198dd9d725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'note', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'note', type_='foreignkey')
    # ### end Alembic commands ###
