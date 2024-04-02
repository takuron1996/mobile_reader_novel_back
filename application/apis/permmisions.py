"""権限絡みのモジュール."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config.environment import jwt_settings

bearer_security = HTTPBearer()


def check_access_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(bearer_security)
    ]
) -> int:
    """アクセストークンを取得してuser_idを返却."""
    access_token = credentials.credentials
    try:
        payload = jwt.decode(
            access_token,
            jwt_settings.JWT_SECRET_ACCESS_KEY,
            algorithms=jwt_settings.JWT_ALGORITHM,
        )
        user_id = payload.get("sub")
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_token",
                "error_description": "トークンの認証エラー。",
            },
        )
