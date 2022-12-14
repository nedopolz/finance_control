"""fk fix

Revision ID: 789977fb08d3
Revises: c8f78c2330f9
Create Date: 2022-11-13 13:04:07.804711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "789977fb08d3"
down_revision = "c8f78c2330f9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("accounts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.alter_column("accounts", "type_id", existing_type=sa.INTEGER(), nullable=False)
    op.create_foreign_key(None, "accounts", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "accounts", type_="foreignkey")
    op.alter_column("accounts", "type_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("accounts", "user_id")
    # ### end Alembic commands ###
