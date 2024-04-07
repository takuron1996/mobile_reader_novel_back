"""署名関連のモジュール."""

import hashlib
import hmac
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import Header, Request, status

from apis.exception import ErrorHttpException
from config.environment import settings


async def verify_signature(
    request: Request, signature: str = Header(alias="Signature")
):
    """署名を検証."""
    url = request.url
    if not hmac.compare_digest(
        signature,
        create_signature(
            request.method, f"{url.scheme}://{url.netloc}{url.path}"
        ),
    ):
        raise ErrorHttpException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="invalid_signature",
            error_description="署名が間違っています。",
        )


def create_signature(
    method,
    url,
) -> str:
    """指定されたHTTPメソッド、URL、および日付を用いて、APIリクエストの署名を生成します。.

    この関数は、HTTPメソッド（GET, POSTなど）、リクエストされるURL、
    そしてオプショナルな日付（デフォルトでは現在の日付が使用されます）を引数として受け取り、
    これらの情報から正規リクエストを作成します。正規リクエストはSHA-256を用いてハッシュ化され、
    その後、設定ファイルから取得したAPIキーを使ってHMACを用いた署名が計算されます。
    Args:
        method (str): HTTPリクエストメソッド（例：'GET', 'POST'）。
        url (str): リクエストされるリソースのURL。
        デフォルトでは現在の日付（東京のタイムゾーン）。
    Returns:
        str: 生成された署名（16進数の文字列）。.
    """
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
    # 正規リクエストの作成
    canonical_request = f"{method}\n{url}\n{now}"
    # 正規リクエストのハッシュ化
    signature_string = hashlib.sha256(canonical_request.encode()).digest()
    # 署名の計算
    signature = hmac.new(
        settings.API_KEY.encode(), signature_string, hashlib.sha256
    ).hexdigest()
    return signature
