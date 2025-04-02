import logging
import uuid
from typing import Optional, Annotated
from datetime import datetime
from decimal import Decimal

from fastapi import Depends, HTTPException, status

# 建立 Database Table
from ..database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 驗證 Request
from pydantic import BaseModel

from llm.utils.auth import bcrypt_context
from llm.utils.newHTTPException import NewHTTPException

# log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################

# 基於 Base class 建立 Users class (Table)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=str(uuid.uuid4()), unique=True, nullable=False)
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

class Token(BaseModel):
    access_token: str
    token_type: str


# async def query_set_to_dict(query_set, conv=False):
#     obj_dict = {}
#     for column in query_set.columns.keys():
#         value = getattr(query_set, column)
#         if isinstance(value, Decimal):
#             value = float(value)
#         if isinstance(value, datetime):
#             if conv:
#                 value = timestamp(seconds=int(value.timestamp()))
#             else:
#                 value = value.strftime("%Y-%m-%d %H:%M:%S")
#         obj_dict[column] = value
#     return obj_dict



# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

class UsersTable:
    # 使用 class 內的函數時，必須加上 self 參數，不然會產生 takes 1 positional argument but 2 were given 錯誤
    # # 跟直接使用 def 的函數時用法不一樣
    async def insert_new_user(self, create_user_request):
        try:
            # 用 with 管理資源的獲取跟釋放
            with get_db() as db:
                create_user_model = User(
                    email=create_user_request.email,
                    username=create_user_request.username,
                    first_name=create_user_request.first_name,
                    last_name=create_user_request.last_name,
                    role=create_user_request.role,
                    hashed_password=bcrypt_context.hash(create_user_request.password),
                    is_active=True,
                    phone_number=create_user_request.phone_number
                )
                # print(create_user_model)
                db.add(create_user_model)
                db.commit()

        except SQLAlchemyError as e:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )


    async def get_users(self):
        try:
            with get_db() as db:
                query = text("SELECT * FROM users")
                result = db.execute(query)
                # sqlalchemy Object 需要轉成 dict

                if result is None:
                    return None

            users = [{
                        "id": row.id,
                        "uuid": row.uuid,
                        "email": row.email,
                        "username": row.username,
                        "first_name": row.first_name,
                        "last_name": row.last_name,
                        "role": row.role,
                        "phone_number": row.phone_number
                        } for row in result
                    ]

            return users

        except SQLAlchemyError as e:
            raise NewHTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User not found",
                msg=str(e)
            )

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

    async def get_user_by_id(self, user_id):
        try:
            with get_db() as db:
                query = text("SELECT * FROM users WHERE id = :user_id")
                result = db.execute(query, {"user_id": user_id})
                # sqlalchemy Object 需要轉成 dict
                row = result.fetchone()

                if row is None:
                    return None

                user = {
                    "id": row.id,
                    "uuid": row.uuid,
                    "email": row.email,
                    "username": row.username,
                    "first_name": row.first_name,
                    "last_name": row.last_name,
                    "role": row.role,
                    "phone_number": row.phone_number
                }

                return user

        except SQLAlchemyError as e:
            raise NewHTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User not found",
                msg=str(e)
            )
        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

Users = UsersTable()