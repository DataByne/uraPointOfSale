"""empty message

Revision ID: a8703695be20
Revises: 99b924574c69
Create Date: 2019-12-04 17:12:25.320027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8703695be20'
down_revision = '99b924574c69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('public_note', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_note_public_note'), 'note', ['public_note'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_note_public_note'), table_name='note')
    op.drop_column('note', 'public_note')
    # ### end Alembic commands ###