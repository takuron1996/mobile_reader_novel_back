"""FastAPIのエントリーポイント."""


from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from apis.exception import ErrorHttpException
from config.config import setup_middlewares
from routers import router

app = FastAPI()
"""FastAPIのインスタンス"""

setup_middlewares(app)

app.include_router(router)


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
