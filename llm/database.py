from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from llm.utils.dotenv import *

sqlite_path = os.getenv("SQLALCHEMY_SQLITE_DATABASE_URL")

# 建立 SQLAlchemy 的 database URL
# SQLite3
SQLALCHEMY_DATABASE_URL = sqlite_path
# PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/TodoApplicationDatabase"
# MySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12341234!@127.0.0.1:3306/TodoApplicationDatabase"

# 建立 engine
# 預設 SQLite 只允許一個線程連線，為了防止不同線程同時存取 database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 建立 engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 與資料庫建立 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 SQLAlchemy Base class
Base = declarative_base()
