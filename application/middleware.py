"""ミドルウェア用のモジュール."""
import hmac

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from apis.exception import ErrorHttpException
from apis.signature import create_signature


class SignatureMiddleware(BaseHTTPMiddleware):
    """署名を確認するミドルウェア."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """ミドルウェアの処理."""
        error_exception = ErrorHttpException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="invalid_signature",
            error_description="署名が間違っています。",
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


class ErrorMiddleware(BaseHTTPMiddleware):
    """エラー発生時に適用するミドルウェア."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """ミドルウェアの処理"""
        try:
            response: Response = await call_next(request)
        except ErrorHttpException as exc:
            print(exc.detail)
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail,
            )
        return response
