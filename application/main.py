"""FastAPIのエントリーポイント."""


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


@app.exception_handler(RequestValidationError)
async def error_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """バリデーションエラーのメッセージを整形するハンドラー."""
    _, msg = exc.errors()[0].get("msg").split(", ")
    print(msg)
    detail = {"error": "validation_error", "error_description": msg}
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
