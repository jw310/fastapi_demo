from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,  nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    phone_number = Column(String)

# 基於 Base class 建立 Todos class (Table)
class Todos(Base):
    # 定義 table 名稱
    __tablename__ = "todos"
    # 定義 Column
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, nullable=False, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))