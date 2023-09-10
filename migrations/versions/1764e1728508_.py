"""empty message

Revision ID: 1764e1728508
Revises: 798594e59281
Create Date: 2023-09-10 11:05:06.472465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1764e1728508'
down_revision = '798594e59281'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('snippets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('snippets', schema=None) as batch_op:
        batch_op.drop_column('code')

    # ### end Alembic commands ###
