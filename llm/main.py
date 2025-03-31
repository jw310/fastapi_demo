# from typing import Any, Dict, Union
from fastapi import FastAPI, Request, status
from starlette.applications import Starlette
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import time
import os
import uuid

### 處理 middleware ###
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

### HTML 模板引擎 ###
from fastapi.templating import Jinja2Templates
# # 載入靜態檔案
from fastapi.staticfiles import StaticFiles


### 處理 routers ### .routers 同層的 routers 目錄引入
from .routes import auths

### Log 處理 ###
from .log import init_logging
# import logging

logger = init_logging()

# 開關 cmd 預設 log 資訊
# logger_ac = logging.getLogger("uvicorn.access")
# logger_ac.handlers = []

### 自定義的 NewHTTPException ###
from llm.utils.newHTTPException import NewHTTPException

### 資料庫 ###
from .database import engine
from .models import Base

from llm.env import BASE_DIR


# load_dotenv(dotenv_path='.env')

### Middleware API 時間計算 ###
class CalcApiTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()

CORS_ALLOW_ORIGINS = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CalcApiTimeMiddleware
)

app.include_router(auths.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)


# main.py 執行時 建立 database 及 tables
Base.metadata.create_all(bind=engine)

# 使用 自定義的 NewHTTPException
@app.exception_handler(NewHTTPException)
async def http_exception_handler(request: Request, exc: NewHTTPException):
    print("Error:", exc.msg)   # 紀錄可預期的錯誤的 log
    logger.error(exc.msg)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

### Middleware ###

### API Error 處理 ###
@app.middleware("http")
async def get_request(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code < 400:
            logger.info('Info')
        return response
    except Exception as e:     # 非預期的錯誤
        print("Error:", e)     # 紀錄非預期的錯誤的 log
        logger.error('Error:', e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

### 每個請求新增唯一的 request ID ###
# @app.middleware("http")
# async def add_request_id(request: Request, call_next):
#     request_id = str(uuid.uuid4())
#     request.state.request_id = request_id
#     response = await call_next(request)
#     response.headers["X-Request-ID"] = request_id
#     return response

### 可以在此進行 IP 驗證、速率限制等安全檢查 ###
# @app.middleware("http")
# async def security_middleware(request: Request, call_next):
#     if request.client.host == "blocked_ip":
#         return JSONResponse(
#             status_code=403,
#             content={"message": "Access Denied"}
#         )
#     return await call_next(request)


# 建立 Jinja2 模板引擎
templates = Jinja2Templates(directory=BASE_DIR / 'templates')
# 載入靜態檔案
app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')


### endpoints ###

# 檢查 app 是否正常啟動
@app.get('/healthy')
def health_check():
    try:
        return {'status': 'Healthy'}
    except NameError as e:
        raise NewHTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail="Internal Server Error", msg=str(e))

# 模擬 API 耗時操作
@app.get("/slow")
async def slow_endpoint():
    time.sleep(1)
    return {"message": "Slow endpoint processed"}

# 在命令列中直接執行 python main.py 來啟動 FastAPI
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)