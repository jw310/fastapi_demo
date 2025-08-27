import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from contextlib import contextmanager

from llm.env import DATABASE_URL, TEST_DATABASE_URL

# 建立 SQLAlchemy 的 database URL
DATABASE_URL = DATABASE_URL

if os.getenv("SWITCH_TEST_DATABASE") == "true":
    DATABASE_URL = TEST_DATABASE_URL

# def get_sqlalchemy_db_url() -> str:
#     db_user = DB_USERNAME
#     db_pass = DB_PASSWORD
#     db_host = DB_HOST
#     db_port = DB_PORT
#     db_name = DB_NAME
#     sqlalchemy_db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
#     return sqlalchemy_db_url

# 建立 engine
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        # 預設 SQLite 只允許一個線程連線，為了防止不同線程同時存取 database
        connect_args={"check_same_thread": False},
        # 建立 engine echo 在 cmd 上顯示所有執行的過程
        echo=False
    )
# else:
#     if DATABASE_POOL_SIZE > 0:
#         engine = create_engine(
#             DATABASE_URL,
#             pool_size=DATABASE_POOL_SIZE,
#             max_overflow=DATABASE_POOL_MAX_OVERFLOW,
#             pool_timeout=DATABASE_POOL_TIMEOUT,
#             pool_recycle=DATABASE_POOL_RECYCLE,
#             pool_pre_ping=True,
#             poolclass=QueuePool,
#         )
#     else:
#         engine = create_engine(
#             DATABASE_URL, pool_pre_ping=True, poolclass=NullPool
#         )

# 與資料庫建立 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 SQLAlchemy Base class，可以定義專門被繼承的通用 Base class
class Base(DeclarativeBase):
    pass

# send request 之前只執行 yield 之前的程式碼
# 發送之後執行 yield 之後的程式碼
def get_session():
    # 資料庫建立一個本機 session，跟資料庫連線
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 自定義交易範圍管理器
@contextmanager
def transaction_scope():
    """提供交易範圍的上下文管理器"""
    db = SessionLocal()
    try:
        yield
        db.commit()
        # logger.info("Transaction committed successfully")
    except Exception:
        db.rollback()
        # logger.error(f"Transaction rolled back due to error: {str(e)}")
        raise

# 將 get_db 定義為 contextmanager 物件
get_db = contextmanager(get_session)

# 確保 get_db 是一個 generator function
# FastAPI 的 Depends() 期望一個 generator function，而不是 contextmanager 物件
# get_db = get_session