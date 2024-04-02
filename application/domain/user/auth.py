"""このモジュールは、トークン認証の機能を提供します."""
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config.environment import jwt_settings
from crud import get_email_user, get_id_user
from models.user import User
from schemas.user import AuthUserResponse


async def create_token(db: AsyncSession, user_id: str) -> AuthUserResponse:
    """アクセストークン及びリフレッシュトークンを生成する関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためのユーザー情報。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """
    minutes = timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    month = timedelta(days=jwt_settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(ZoneInfo("Asia/Tokyo")) + minutes
    refresh_expire = datetime.now(ZoneInfo("Asia/Tokyo")) + month
    access_token = jwt.encode(
        {"sub": user_id, "exp": expire},
        jwt_settings.JWT_SECRET_ACCESS_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    refresh_token = jwt.encode(
        {"sub": user_id, "exp": refresh_expire},
        jwt_settings.JWT_SECRET_REFRESH_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )

    user = await get_id_user(db, int(user_id))
    user.set_refresh_token(refresh_token)
    db.add(user)
    await db.commit()

    return AuthUserResponse(
        access_token=access_token, refresh_token=refresh_token
    )


async def auth_password(
    db: AsyncSession,
    email: str,
    password: str,
) -> AuthUserResponse:
    """id/passwordによる認証を行う関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためユーザー情報。
    - async_session (AsyncSession): DBとのセッション。

    Returns:
    - create_tokenのレスポンス
    """

    def authenticate_user(user: Optional[User]):
        if user is None:
            return False
        return user.check_password(password)

    user = await get_email_user(db, email)

    if not authenticate_user(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "bad_request",
                "error_description": "メールアドレスかpasswordが異なります",
            },
        )

    return await create_token(db, str(user.id))


async def auth_token(db: AsyncSession, refresh_token: str) -> AuthUserResponse:
    """リフレッシュトークンによる認証を行う関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためのユーザー情報。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """
    try:
        payload = jwt.decode(
            refresh_token,
            jwt_settings.JWT_SECRET_REFRESH_KEY,
            algorithms=jwt_settings.JWT_ALGORITHM,
        )
        user_id = payload.get("sub")
        user = await get_id_user(db, int(user_id))
        if not user.check_refresh_token(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "invalid_token",
                    "error_description": "不正なリフレッシュトークンです",
                },
            )
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "unknown_user",
                    "error_description": "不明なユーザーです",
                },
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_token",
                "error_description": "アクセストークンの有効期限切れです。",
            },
        )

    return await create_token(db, user_id)
