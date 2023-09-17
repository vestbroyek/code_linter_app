"""empty message

Revision ID: 798594e59281
Revises: 
Create Date: 2023-09-07 17:50:29.319310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "798594e59281"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_link", sa.String(), nullable=True),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "snippets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("snippets")
    op.drop_table("projects")
    # ### end Alembic commands ###
