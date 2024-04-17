"""ルーター用モジュール."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from apis.exception import ErrorHttpException
from apis.permmisions import check_access_token
from apis.signature import verify_signature
from config.config import get_async_session
from domain.narou.follow import delete_follow, post_follow
from domain.narou.main_text import get_main_text
from domain.narou.novel_info import get_novel_info
from domain.user.auth import auth_password, auth_token
from domain.user.resistration import user_resistration
from schemas.follow import FollowModel, FollowResponse
from schemas.novel import NovelInfoResponse, NovelResponse
from schemas.token import AuthUserModel, AuthUserResponse, GrantType
from schemas.user import UserRegistrationModel, UserRegistrationResponse

router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
    summary="本文取得API",
    description="指定されたNコードとエピソード番号から小説本文に関する情報を取得します。",
    tags=["小説表示画面"],
)
async def main_text(
    *,
    ncode: str,
    episode: int,
    async_session: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
    user_id: str = Depends(check_access_token),
):
    """小説取得APIのエンドポイント."""
    return await get_main_text(ncode, episode, user_id, async_session)


@router.get(
    "/api/novelinfo",
    response_model=NovelInfoResponse,
    summary="小説情報取得API",
    description="指定されたNコードから目次ページに関する情報を取得します。",
    tags=["目次画面"],
)
async def novel_info(
    ncode: str,
    db: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
    user_id: str = Depends(check_access_token),
):
    """小説情報取得APIのエンドポイント."""
    return await get_novel_info(db, ncode, user_id)


@router.post(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り登録API",
    description="指定されたNコードをお気に入り登録します。",
    tags=["お気に入り"],
)
async def post_follow_router(
    follow_model: FollowModel,
    db: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
    user_id: str = Depends(check_access_token),
):
    """お気に入り登録APIのエンドポイント."""
    return await post_follow(db, follow_model.ncode, user_id)


@router.delete(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り削除API",
    description="指定されたNコードをお気に入り削除します。",
    tags=["お気に入り"],
)
async def delete_follow_router(
    follow_model: FollowModel,
    db: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
    user_id: str = Depends(check_access_token),
):
    """お気に入り削除APIのエンドポイント."""
    return await delete_follow(db, follow_model.ncode, user_id)


@router.post(
    "/api/token",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    summary="ログイン認証・トークン生成API",
    description="ID/パスワードorリフレッシュトークンによる認証を行い新たなアクセストークンとリフレッシュトークンを発行します。",
    tags=["token"],
)
async def auth_token_router(
    auth_data: AuthUserModel,
    db: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
):
    """ログイン認証・トークン生成APIのエンドポイント."""
    match auth_data.grant_type:
        case GrantType.PASSWORD.value:
            if None in {auth_data.id, auth_data.password}:
                raise ErrorHttpException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error="invalid_parameter",
                    error_description="user_id と password は必須となります。",
                )
            return await auth_password(
                email=auth_data.id,
                password=auth_data.password,
                db=db,
            )
        case GrantType.REFRESH_TOKEN.value:
            if auth_data.refresh_token is None:
                raise ErrorHttpException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error="invalid_parameter",
                    error_description="refresh_token は必須となります。",
                )
            return await auth_token(
                db=db, refresh_token=auth_data.refresh_token
            )
        case _:
            raise ErrorHttpException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error="invalid_parameter",
                error_description="grant_typeが不明です。",
            )


@router.post(
    "/api/user",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_200_OK,
    summary="ユーザー登録API",
    description="ユーザー登録を実施。",
    tags=["user"],
)
async def user_resistration_router(
    user_data: UserRegistrationModel,
    db: AsyncSession = Depends(get_async_session),
    signature=Depends(verify_signature),
):
    """ユーザー登録APIのエンドポイント."""
    is_success = await user_resistration(db, user_data)
    return UserRegistrationResponse(is_success=is_success)
