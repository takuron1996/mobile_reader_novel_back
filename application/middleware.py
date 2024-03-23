"""ミドルウェア用のモジュール."""
import hmac

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from apis.signature import create_signature


class SignatureMiddleware(BaseHTTPMiddleware):
    """署名を確認するミドルウェア."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """ミドルウェアの処理."""
        error_response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
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
            return error_response

        url = request.url
        if not hmac.compare_digest(
            signature,
            create_signature(
                request.method, f"{url.scheme}://{url.netloc}{url.path}"
            ),
        ):
            return error_response

        return await call_next(request)
