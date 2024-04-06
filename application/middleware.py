"""ミドルウェア用のモジュール."""
import hmac

from fastapi import Request, Response, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from apis.signature import create_signature


class SignatureMiddleware(BaseHTTPMiddleware):
    """署名を確認するミドルウェア."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """ミドルウェアの処理."""
        error_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "signature_error",
                    "error_description": "署名が間違っています。",
                },
            )

        # SwaggerUIへのアクセスだけ除外
        if request.url.path in {"/docs", "/openapi.json"}:
            return await call_next(request)

        # 署名検証
        signature = request.headers.get("Signature")
        if signature is None:
            raise error_exception

        url = request.url
        if not hmac.compare_digest(
            signature,
            create_signature(
                request.method, f"{url.scheme}://{url.netloc}{url.path}"
            ),
        ):
            raise error_exception

        return await call_next(request)
