from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from models.book import Book
from models.read_history import ReadHistory
from models.follow import Follow

async def ensure_book_exists(db: AsyncSession, ncode: str) -> int:
    """
    指定されたncodeに基づいてBookテーブルを検索し、存在しない場合は新規追加する関数。
    追加または検索によって得られたbook_idを返す。
    """
    # Bookテーブルからncodeに対応するbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_record = book_result.scalars().first()

    # 指定されたncodeの小説情報が存在しない場合、新規追加する
    if not book_record:
        new_book = Book(ncode=ncode)
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book.id
    else:
        return book_record

async def insert_read_history_if_not_exists(db: AsyncSession, book_id: int, episode: int):
    """
    指定されたbook_idとエピソードに対応する既読情報が存在しなければ、データを挿入する関数。
    """
    stmt = (
        insert(ReadHistory).
        values(book_id=book_id, read_episode=episode).
        on_conflict_do_nothing(index_elements=['book_id', 'read_episode'])
    )
    await db.execute(stmt)
    await db.commit()

async def get_read_episode_by_ncode(db: AsyncSession, ncode: str) -> int:
    """
    指定されたncodeに基づいてread_episodeの値を非同期で取得する関数。
    """
    # Bookテーブルからncodeに基づくbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    if book_id is None:
        return 0

    # ReadHistoryからbook_idに基づくread_episodeの最大値を取得
    query = select(func.max(ReadHistory.read_episode)).filter(ReadHistory.book_id == book_id)
    result = await db.execute(query)
    max_read_episode = result.scalars().first()

    return max_read_episode if max_read_episode is not None else 0


async def get_follow_status_by_ncode(db: AsyncSession, ncode: str) -> bool:
    """
    指定されたncodeに基づいてfollowの値を非同期で取得する関数。
    """
    # Bookテーブルからncodeに基づくbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    if book_id is None:
        return False

    # Followテーブルからbook_idに基づくis_followステータスを取得
    query_follow_status = select(Follow.is_follow).filter(Follow.book_id == book_id)
    result_follow_status = await db.execute(query_follow_status)
    follow_status = result_follow_status.scalars().first()

    return follow_status if follow_status is not None else False
