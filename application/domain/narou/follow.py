"""このモジュールは、お気に入りの設定や解除に関する非同期関数を提供します.

特定の小説のお気に入り設定（フォロー）と解除（アンフォロー）の機能が含まれています。
"""
from bs4 import BeautifulSoup
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apis.exception import ErrorHttpException
from apis.request import request_get
from apis.urls import Url
from apis.user_agent import UserAgentManager
from crud import (
    create_or_check_existing_follow,
    delete_follow_by_book_id,
    ensure_book_exists,
)
from models.book import Book
from models.follow import Follow
from models.read_history import ReadHistory
from schemas.follow import FollowResponse, GetFollowResponse


async def post_follow(db: AsyncSession, ncode: str, user_id: str):
    """指定されたncodeに基づいて小説の情報を取得し、それをお気に入りに設定する関数."""
    # Bookテーブルからncodeに対応するbook_idを取得。
    book_id = await ensure_book_exists(db, ncode)
    # Followテーブルを検索し、boolを返す。
    is_follow = not await create_or_check_existing_follow(db, book_id, user_id)

    return FollowResponse(is_success=is_follow)


async def delete_follow(db: AsyncSession, ncode: str, user_id: str):
    """指定されたncodeに基づいて小説の情報を取得し、それをお気に入りから削除する関数."""
    # Bookテーブルからncodeに対応するbook_idを取得
    book_id = await ensure_book_exists(db, ncode)
    # Followテーブルで対応するエントリを検索し、削除する
    is_success = await delete_follow_by_book_id(db, book_id, user_id)

    return FollowResponse(is_success=is_success)


async def get_follow(db: AsyncSession, user_id: str):
    """お気に入り取得APIのロジック."""
    # お気に入りの小説のbook.idを取得
    query = select(Follow.book_id).where(Follow.user_id == user_id)
    result = await db.execute(query)
    ids = result.scalars().all()
    if not ids:
        return []

    # ncodeを取得
    query = select(Book).where(Book.id.in_(ids)).order_by(Book.id)
    result = await db.execute(query)
    books = result.scalars().all()

    # 小説家になろうから情報を取得
    headers = UserAgentManager().get_random_user_headers()
    result_response = []
    for book in books:
        ncode = book.ncode
        novel_url = Url.NOVEL_URL.join(ncode)
        response = request_get(novel_url, headers)
        if response is None:
            raise ErrorHttpException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error="server_error",
                error_description="小説情報の取得に失敗しました。",
            )
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find(class_="novel_title").get_text()
        author = soup.find(class_="novel_writername").find("a").get_text()

        # 既読情報を取得
        query = select(ReadHistory.read_episode).filter(
            ReadHistory.book_id == book.id, ReadHistory.user_id == user_id
        )
        result = await db.execute(query)
        episode = result.scalar_one_or_none()
        if episode is None:
            episode = 1

        result_response.append(
            GetFollowResponse(
                ncode=ncode, title=title, author=author, read_episode=episode
            )
        )

    return result_response
