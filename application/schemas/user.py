"""ユーザーAPI関連のスキーマ用モジュール."""

from pydantic import BaseModel, Field

from validators import Email, Password


class UserRegistrationModel(BaseModel):
    """ユーザーAPIで使用するバリデーションモデル."""

    email: Email = Field(
        title="メールアドレス",
        description="ユーザー自身が設定したメールアドレス",
        example="test01@example.com",
    )
    password: Password = Field(
        title="パスワード",
        description="パスワード",
        example="Password1",
    )
