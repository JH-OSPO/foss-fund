"""Add end_date to campaigns

Revision ID: 9c82ddf00582
Revises: 5808a44f2fd3
Create Date: 2021-07-28 00:24:35.458405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c82ddf00582'
down_revision = '5808a44f2fd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campaigns', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campaigns', schema=None) as batch_op:
        batch_op.drop_column('end_date')

    # ### end Alembic commands ###
