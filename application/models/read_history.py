"""このモジュールは、ユーザーの既読情報を表すためのデータベースモデルを提供します."""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ReadHistory(Base):
    """既読テーブルのORM."""

    __tablename__ = "read_history"
    __table_args__ = (UniqueConstraint("book_id", "user_id"),)

    book_id = Column(String(26), ForeignKey("book.id"), nullable=False)
    read_episode: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="既読した話数"
    )
    user_id = Column(String(26), ForeignKey("user.id"), nullable=False)

    # Relationshipの定義
    book = relationship("Book", back_populates="read_history", uselist=True)
    user = relationship("User", back_populates="read_history", uselist=True)
