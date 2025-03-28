import logging
import uuid
from typing import Optional

# 建立 Database Table
from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean

# 驗證 Request
from pydantic import BaseModel

# log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################

# 基於 Base class 建立 Users class (Table)
class User(Base):
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


####################
# Request、Forms
####################

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str



class UsersTable:
    # 寫資料庫操作方式，用從 router 傳入參數給這裡的函數
    async def insert_new_user():
        pass



Users = UsersTable()