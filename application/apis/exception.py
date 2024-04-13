"""カスタムエラークラス用のモジュール."""

from fastapi import HTTPException
from pydantic_core import PydanticCustomError


class ErrorHttpException(HTTPException):
    """エラー発生時のカスタム例外クラス."""

    def __init__(self, status_code: int, error: str, error_description: str):
        """初期化."""
        detail = {"error": error, "error_description": error_description}
        super().__init__(status_code=status_code, detail=detail)


def get_validation_exception(msg: str) -> PydanticCustomError:
    """バリデーション発生時のエラーを取得."""
    return PydanticCustomError("validation_error", msg)
