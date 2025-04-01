import logging
import uuid
from typing import Optional, Annotated

from fastapi import Depends

# 建立 Database Table
from ..database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

# 驗證 Request
from pydantic import BaseModel

from llm.utils.auth import bcrypt_context

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

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 使用 class 內的函數時，必須加上 self 參數，不然產生 takes 1 positional argument but 2 were given 錯誤
# 跟直接使用 def 的函數不一樣
class UsersTable:
    # 寫資料庫操作方式，用從 router 傳入參數給這裡的函數
    async def insert_new_user(self, create_user_request):
        try:
            # 用 with 管理資源的獲取跟釋放
            with get_db() as db:
                # user = db.query(User).filter_by(id=id).first()
                # return UserModel.model_validate(user)
                create_user_model = Users(
                    email=create_user_request.email,
                    username=create_user_request.username,
                    first_name=create_user_request.first_name,
                    last_name=create_user_request.last_name,
                    role=create_user_request.role,
                    hashed_password=bcrypt_context.hash(create_user_request.password),
                    is_active=True,
                    phone_number=create_user_request.phone_number
                )

            db.add(create_user_model)
            db.commit()

        except Exception:
            return None


Users = UsersTable()