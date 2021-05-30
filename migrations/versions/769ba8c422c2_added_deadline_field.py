"""added deadline field

Revision ID: 769ba8c422c2
Revises: 33b3dc178ac4
Create Date: 2021-05-29 13:39:38.093312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '769ba8c422c2'
down_revision = '33b3dc178ac4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('deadline', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_task_deadline'), 'task', ['deadline'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_deadline'), table_name='task')
    op.drop_column('task', 'deadline')
    # ### end Alembic commands ###