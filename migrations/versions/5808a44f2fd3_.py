"""empty message

Revision ID: 5808a44f2fd3
Revises: c06463b9bcbc
Create Date: 2021-04-05 09:15:38.778956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5808a44f2fd3'
down_revision = 'c06463b9bcbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###