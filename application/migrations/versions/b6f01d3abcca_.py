"""empty message

Revision ID: b6f01d3abcca
Revises: 
Create Date: 2024-04-17 14:29:38.297975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6f01d3abcca"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column(
            "ncode", sa.String(length=255), nullable=False, comment="小説コード"
        ),
        sa.Column("id", sa.String(length=26), nullable=False, comment="ID"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ncode"),
    )
    op.create_table(
        "user",
        sa.Column(
            "email", sa.String(length=254), nullable=False, comment="メールアドレス"
        ),
        sa.Column("refresh_token", sa.String(length=60), nullable=True),
        sa.Column("id", sa.String(length=26), nullable=False, comment="ID"),
        sa.Column("password", sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "follow",
        sa.Column("book_id", sa.String(length=26), nullable=False),
        sa.Column("user_id", sa.String(length=26), nullable=False),
        sa.Column("id", sa.String(length=26), nullable=False, comment="ID"),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "user_id"),
    )
    op.create_table(
        "read_history",
        sa.Column("book_id", sa.String(length=26), nullable=False),
        sa.Column(
            "read_episode", sa.Integer(), nullable=False, comment="既読した話数"
        ),
        sa.Column("user_id", sa.String(length=26), nullable=False),
        sa.Column("id", sa.String(length=26), nullable=False, comment="ID"),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("read_history")
    op.drop_table("follow")
    op.drop_table("user")
    op.drop_table("book")
    # ### end Alembic commands ###
