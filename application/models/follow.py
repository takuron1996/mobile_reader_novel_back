"""このモジュールは、ユーザーのお気に入り（フォロー）情報を表すためのデータベースモデルを提供します."""
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from models.base import Base


class Follow(Base):
    """お気に入りテーブルのORM."""

    __tablename__ = "follow"
    __table_args__ = (UniqueConstraint("book_id", "user_id"),)

    book_id = Column(
        Integer, ForeignKey("book.id"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("user.id"), nullable=False
    )

    # Relationshipの定義
    book = relationship("Book", back_populates="follow", uselist=False)
    user = relationship("User", back_populates="follow", uselist=False)
