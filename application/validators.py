"""バリデータ関連のモジュール."""

import re
from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from pydantic import AfterValidator

from apis.exception import get_validation_exception

PASSWORD_PATTERN = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")


def check_email(value: str) -> str:
    """emailのカスタムバリデータ."""
    try:
        emailinfo = validate_email(value, check_deliverability=False)
        email = emailinfo.normalized
    except EmailNotValidError as exc:
        print(exc)
        raise get_validation_exception("指定されたemailは使用することはできません")
    return email


def check_password(value: str) -> str:
    """パスワードのカスタムバリデータ."""
    if not PASSWORD_PATTERN.fullmatch(value):
        raise get_validation_exception("パスワードの要件を満たしていません")
    return value


Password = Annotated[
    str,
    AfterValidator(check_password),
]

Email = Annotated[
    str,
    AfterValidator(check_email),
]
