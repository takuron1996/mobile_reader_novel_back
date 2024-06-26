"""このモジュールは、お気に入り関連の操作に関するレスポンスモデルを定義しています."""
from pydantic import BaseModel, Field


class FollowModel(BaseModel):
    """フォローで使用するバリデーションモデル."""

    ncode: str = Field(
        title="ncode",
        description="フォロー機能で使用したいncode",
        example="n9690ip",
    )


class FollowResponse(BaseModel):
    """お気に入り処理の成功状態を示すレスポンスモデル.

    このモデルは、お気に入り登録または削除のAPIレスポンスとして使用されます。
    処理が成功した場合、`is_success` は `True` に設定されます。

    属性:
        is_success (bool): お気に入り処理が成功したかどうか。
                           成功した場合は `True`、そうでない場合は `False`。
    """

    is_success: bool = Field(..., title="お気に入り処理が成功してるかどうか")

    class Config:
        """Pydanticモデルの設定クラス.

        json_schema_extra: スキーマの例を定義します。
                        この例はAPIのドキュメントで使用され、
                        APIの使用方法を理解しやすくするために役立ちます。
        """

        json_schema_extra = {"example": {"is_success": True}}


class GetFollowResponse(BaseModel):
    """お気に入り取得APIのレスポンスモデル."""

    ncode: str
    title: str
    author: str
    read_episode: int

    class Config:
        """Pydanticモデルの設定クラス.

        json_schema_extra: スキーマの例を定義します。
                        この例はAPIのドキュメントで使用され、
                        APIの使用方法を理解しやすくするために役立ちます。
        """

        json_schema_extra = {
            "example": {
                "ncode": "xxxx",
                "title": "小説名",
                "author": "作者名",
                "read_episode": 10,
            }
        }
