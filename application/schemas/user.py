"""ユーザーAPI関連のスキーマ用モジュール."""

import re

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, field_validator

PASSWORD_PATTERN = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")


class UserRegistrationModel(BaseModel):
    """ユーザーAPIで使用するバリデーションモデル."""

    email: str = Field(
        title="メールアドレス",
        description="ユーザー自身が設定したメールアドレス",
        example="test01@example.com",
    )
    password: str = Field(
        title="パスワード",
        description="パスワード",
        example="Password1",
    )

    @field_validator("email")
    def validate_email(cls, value):
        """emailのカスタムバリデータ."""
        try:
            emailinfo = validate_email(value, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as exc:
            print(exc)
            raise ValueError("指定されたemailは使用することはできません")
        return email

    @field_validator("password")
    def validate_password(cls, value):
        """パスワードのカスタムバリデータ."""
        if not PASSWORD_PATTERN.fullmatch(value):
            raise ValueError("パスワードの要件を満たしていません")
        return value
