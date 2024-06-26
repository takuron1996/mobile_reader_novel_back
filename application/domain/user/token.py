"""このモジュールは、トークン認証の機能を提供します."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jose import jwt

from config.environment import jwt_settings
from schemas.token import AuthUserResponse


async def create_token(user_id: str) -> AuthUserResponse:
    """アクセストークン及びリフレッシュトークンを生成する関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためのユーザー情報。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """
    hours = timedelta(hours=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    month = timedelta(days=jwt_settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(ZoneInfo("Asia/Tokyo")) + hours
    refresh_expire = datetime.now(ZoneInfo("Asia/Tokyo")) + month
    access_token = jwt.encode(
        {"sub": str(user_id), "exp": expire},
        jwt_settings.JWT_SECRET_ACCESS_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    refresh_token = jwt.encode(
        {"sub": str(user_id), "exp": refresh_expire},
        jwt_settings.JWT_SECRET_REFRESH_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    return AuthUserResponse(
        access_token=access_token, refresh_token=refresh_token
    )
