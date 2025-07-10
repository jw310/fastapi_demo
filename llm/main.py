# from typing import Any, Dict, Union
from fastapi import FastAPI, Request, status, Depends
from starlette.applications import Starlette
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import time
import sys
import uuid
from typing import Annotated
from contextlib import asynccontextmanager

### 處理 middleware ###
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

### HTML 模板引擎 ###
from fastapi.templating import Jinja2Templates
# # 載入靜態檔案
from fastapi.staticfiles import StaticFiles

from llm.env import (
    GLOBAL_LOG_LEVEL,
    SRC_LOG_LEVELS,
    AUDIT_LOG_LEVEL,
    AUDIT_EXCLUDED_PATHS,
    MAX_BODY_LOG_SIZE,
    )

from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db

### 處理 routers ### .routes 同層的 routers 目錄引入
from .routes import auth, files, user, admin, chat

### Log 處理 ###
from .log import init_logging
log = init_logging()

### google cloud storage ###
# from llm.utils.google_cloud_storage import *

### 執行測試檔 ###
from llm.utils.test import *

# from llm.utils.transcribe_speech import pipe
# print(pipe)

# import logging
# from llm.utils import logger
# from llm.utils.audit import AuditLevel, AuditLoggingMiddleware
# from llm.utils.logger import start_logger

# logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOG_LEVEL)
# log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["MAIN"])

# 開關 cmd 預設 log 資訊
# logger_ac = logging.getLogger("uvicorn.access")
# logger_ac.handlers = []

### 自定義的 NewHTTPException ###
from llm.utils.newHTTPException import NewHTTPException

### 資料庫 ###
from .database import Base, engine
# from .models import Base

from llm.env import BASE_DIR


##################
### Middleware ###
##################
# app = FastAPI(lifespan=lifespan)
app = FastAPI(title="LLM Gateway API", version="1.0.0")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     start_logger()
#     yield

# try:
#     audit_level = AuditLevel(AUDIT_LOG_LEVEL)
# except ValueError as e:
#     logger.error(f"Invalid audit level: {AUDIT_LOG_LEVEL}. Error: {e}")
#     audit_level = AuditLevel.NONE

# if audit_level != AuditLevel.NONE:
#     app.add_middleware(
#         AuditLoggingMiddleware,
#         audit_level=audit_level,
#         excluded_paths=AUDIT_EXCLUDED_PATHS,
#         max_body_size=MAX_BODY_LOG_SIZE,
#     )

CORS_ALLOW_ORIGINS = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### Middleware API 時間計算 ###
class CalcApiTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


app.add_middleware(
    CalcApiTimeMiddleware
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(admin.router,   prefix="/api/v1/admin", tags=["admin"])
# app.include_router(todos.router)


# 使用 自定義的 NewHTTPException
@app.exception_handler(NewHTTPException)
async def http_exception_handler(request: Request, exc: NewHTTPException):
    print("Error:", exc.msg)   # 紀錄可預期的錯誤的 log
    log.error(exc.msg)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
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

### API Error 處理 ###
# 紀錄非預期的錯誤，但不會回傳詳細資訊給使用者
@app.middleware("http")
async def get_request(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code < 400:
            log.info('Info')
        return response
    except Exception as e:     # 非預期的錯誤
        print("Error:", e)     # 紀錄非預期的錯誤的 log
        log.error('Error:', e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

# main.py 執行時 建立 database 及 tables
Base.metadata.create_all(bind=engine)

# 建立 Jinja2 模板引擎
templates = Jinja2Templates(directory=BASE_DIR / 'templates')
# 載入靜態檔案
app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')


#################
### Endpoints ###
#################
@app.get('/healthy')
def health_check():
    """ check app is running """
    try:
        return {'status': 'Healthy'}
    except NameError as e:
        raise NewHTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail="Internal Server Error", msg=str(e))

@app.get("/healthy/db")
async def health_check_with_db():
    with get_db() as db:
        query = text("SELECT 1")
        result = db.execute(query)
        if result is None:
            return {"status": False}
    return {"status": True}

# 模擬 API 耗時操作
@app.get("/slow")
async def slow_endpoint():
    time.sleep(1)
    return {"message": "Slow endpoint processed"}

# 在命令列中直接執行 python main.py 來啟動 FastAPI
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)