"""add_executor_relation

Revision ID: 9181ae29f34f
Revises: c97b0203d916
Create Date: 2025-06-29 22:40:31.069054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9181ae29f34f'
down_revision = 'c97b0203d916'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('executor_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'user', ['executor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'executor_id')
    # ### end Alembic commands ###
