"""FastAPIのエントリーポイント."""


import time

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from apis.exception import ErrorHttpException
from config.config import setup_middlewares
from routers import router

app = FastAPI()
"""FastAPIのインスタンス"""

setup_middlewares(app)

app.include_router(router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """HTTP通信の開始と終了をロギング."""
    start_time = time.time()
    print(f"接続開始: {request.method} {request.url}")

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"接続終了: {process_time:.4f} secs")

    return response


@app.exception_handler(RequestValidationError)
async def error_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """バリデーションエラーのメッセージを整形するハンドラー."""
    error = exc.errors()[0]
    detail = {"error": error.get("type"), "error_description": error.get("msg")}
    print(detail)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=detail,
    )


@app.exception_handler(ErrorHttpException)
async def error_http_exception_handler(
    request: Request, exc: ErrorHttpException
):
    """エラー発生時にエラー原因をログに出力."""
    print(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )
