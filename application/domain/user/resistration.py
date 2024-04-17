"""ユーザー登録APIのロジックモジュール."""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from apis.exception import ErrorHttpException
from crud import add_user, get_user_by_email
from schemas.user import UserRegistrationModel


async def user_resistration(
    db: AsyncSession, user_data: UserRegistrationModel
) -> bool:
    """ユーザー登録APIのロジック処理."""
    email = user_data.email
    user = await get_user_by_email(db, email)
    if user is not None:
        raise ErrorHttpException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error="validation_error",
            error_description="指定されたemailは使用することはできません",
        )
    await add_user(db, email, user_data.password)
    return True
