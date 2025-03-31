from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager

from llm.env import SQLALCHEMY_DATABASE_URL

# 建立 SQLAlchemy 的 database URL
# SQLite3
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL
# PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/TodoApplicationDatabase"
# MySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12341234!@127.0.0.1:3306/TodoApplicationDatabase"

# 建立 engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# if "sqlite" in SQLALCHEMY_DATABASE_URL:
#     # 預設 SQLite 只允許一個線程連線，為了防止不同線程同時存取 database
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     )
# else:
#     if DATABASE_POOL_SIZE > 0:
#         engine = create_engine(
#             SQLALCHEMY_DATABASE_URL,
#             pool_size=DATABASE_POOL_SIZE,
#             max_overflow=DATABASE_POOL_MAX_OVERFLOW,
#             pool_timeout=DATABASE_POOL_TIMEOUT,
#             pool_recycle=DATABASE_POOL_RECYCLE,
#             pool_pre_ping=True,
#             poolclass=QueuePool,
#         )
#     else:
#         engine = create_engine(
#             SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, poolclass=NullPool
#         )


# 建立 engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 與資料庫建立 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 SQLAlchemy Base class
Base = declarative_base()

# send request 之前只執行 yield 之前的程式碼
# 發送之後執行 yield 之後的程式碼
def get_session():
    # 資料庫建立一個本機 session，跟資料庫連線
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db = contextmanager(get_session)