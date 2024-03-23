"""empty message

Revision ID: d48214f71cd3
Revises: 
Create Date: 2024-02-28 14:21:03.500201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d48214f71cd3"
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
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ncode"),
    )
    op.create_table(
        "follow",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id"),
    )
    op.create_table(
        "read_history",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column(
            "read_episode", sa.Integer(), nullable=False, comment="既読した話数"
        ),
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, comment="ID"
        ),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("book_id"),
        sa.UniqueConstraint("book_id", "read_episode"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("read_history")
    op.drop_table("follow")
    op.drop_table("book")
    # ### end Alembic commands ###