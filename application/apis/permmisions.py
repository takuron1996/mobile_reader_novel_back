"""権限絡みのモジュール."""

from typing import Annotated

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from apis.exception import ErrorHttpException
from config.environment import jwt_settings

bearer_security = HTTPBearer()


def check_access_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(bearer_security)
    ]
) -> str:
    """アクセストークンを取得してuser_idを返却."""
    access_token = credentials.credentials
    try:
        payload = jwt.decode(
            access_token,
            jwt_settings.JWT_SECRET_ACCESS_KEY,
            algorithms=jwt_settings.JWT_ALGORITHM,
        )
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        raise ErrorHttpException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="invalid_token",
            error_description="トークンの認証エラー。",
        )
