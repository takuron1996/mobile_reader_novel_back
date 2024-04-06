"""CustomerテーブルのORM."""

import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, PasswordMixin


class User(Base, PasswordMixin):
    """ユーザーテーブルのORM."""

    from models.follow import Follow
    from models.read_history import ReadHistory

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, comment="メールアドレス"
    )

    _refresh_token: Mapped[str] = mapped_column(
        "refresh_token", String(60), nullable=True
    )

    def set_refresh_token(self, refresh_token):
        """リフレッシュトークンをハッシュ化して設定."""
        refresh_token_bytes = refresh_token.encode("utf-8")
        salt = bcrypt.gensalt()
        self._refresh_token = bcrypt.hashpw(
            password=refresh_token_bytes, salt=salt
        ).decode("utf8")

    def check_refresh_token(self, refresh_token):
        """設定したリフレッシュトークンと一致するかどうかを検証."""
        if self._refresh_token is None:
            return True
        input_refresh_token_hash = refresh_token.encode("utf-8")
        hashed_refresh_token = self._refresh_token.encode("utf-8")
        return bcrypt.checkpw(input_refresh_token_hash, hashed_refresh_token)

    # Relationshipの定義
    read_history = relationship(
        "ReadHistory", back_populates="user", uselist=False
    )
    follow = relationship("Follow", back_populates="user", uselist=False)
