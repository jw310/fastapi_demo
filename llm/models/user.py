import logging
import uuid
from typing import Optional, Annotated
from datetime import datetime
from decimal import Decimal
import math

from fastapi import Depends, HTTPException, status

# 建立 Database Table
from ..database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 驗證 Request
from pydantic import BaseModel

from llm.utils.auth import (bcrypt_context)
from llm.utils.newHTTPException import NewHTTPException
from llm.utils.dictAndObjectCovert import (dict_to_object, object_to_dict)


# log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################

# 基於 Base class 建立 Users class (Table)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False)
    email = Column(String, unique=True,  nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    phone_number = Column(String)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
    Base.to_dict = to_dict

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
    is_active: bool
    phone_number: str

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

class UsersTable:
    # 使用 class 內的函數時，必須加上 self 參數，不然會產生 takes 1 positional argument but 2 were given 錯誤
    # # 跟直接使用 def 的函數時用法不一樣
    async def insert(self, create_user_request):
        try:
            # 用 with 管理資源的獲取跟釋放
            with get_db as db:
                create_user_model = User(
                    uuid=str(uuid.uuid4()),
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

                return True

        except SQLAlchemyError as e:
            raise NewHTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
        )

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

    async def findAll(self, limit: int = 10, page: int = 1):
        try:
            if limit <= 0:
                    limit = 10
            if page <= 0:
                    page = 1

            # 計算 offset
            offset = (page - 1) * limit

            with get_db() as db:

                count_query = text("SELECT COUNT(*) as total FROM users")
                count_result = db.execute(count_query)
                total_count = count_result.scalar()

                if total_count == 0:
                    return {
                        "data": [],
                        "pagination": {
                            "pageSize": limit,
                            "currentPage": page,
                            "totalPages": 0,
                            "totalCount": 0
                        }
                    }

                total_pages = math.ceil(total_count / limit)

                if page > total_pages:
                    page = total_pages
                    offset = (page - 1) * limit

                query = text("""
                    SELECT * FROM users
                    ORDER BY id
                    LIMIT :limit OFFSET :offset
                """)

                result = db.execute(query, {
                    "limit": limit,
                    "offset": offset
                })

                # ORM 用法
                # users_query = db.query(User).order_by(User.id).offset(offset).limit(limit)
                # users = users_query.all()

                if result is None:
                    return None

                users = []

                for row in result:
                    users.append({
                        "id": row.id,
                        "uuid": row.uuid,
                        "email": row.email,
                        "username": row.username,
                        "first_name": row.first_name,
                        "last_name": row.last_name,
                        "hashed_password": row.hashed_password,
                        "role": row.role,
                        "is_active": row.is_active,
                        "phone_number": row.phone_number
                    })

                # users = [{
                #             "id": row.id,
                #             "uuid": row.uuid,
                #             "email": row.email,
                #             "username": row.username,
                #             "first_name": row.first_name,
                #             "last_name": row.last_name,
                #             "hashed_password": row.hashed_password,
                #             "role": row.role,
                #             "is_active": row.is_active,
                #             "phone_number": row.phone_number
                #             } for row in result
                #         ]

            return {
                "data": users,
                "pagination": {
                    "pageSize": limit,
                    "currentPage": page,
                    "totalPages": total_pages,
                    "totalCount": total_count
                }
            }

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

    async def findById(self, id):
        try:
            with get_db() as db:
                query = text("SELECT * FROM users WHERE id = :id")
                result = db.execute(query, {"id": id})
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
                    "hashed_password": row.hashed_password,
                    "role": row.role,
                    "is_active": row.is_active,
                    "phone_number": row.phone_number
                }

                user = dict_to_object(user)

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

    async def findByName(self, username):
        try:
            with get_db() as db:
                query = text("SELECT * FROM users WHERE username = :username")
                result = db.execute(query, {"username": username})
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
                    "hashed_password": row.hashed_password,
                    "role": row.role,
                    "phone_number": row.phone_number
                }

                user = dict_to_object(user)

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

    async def deleteById(self, id):
        try:
            with get_db() as db:
                delete_user = db.query(User).filter(User.id == id).first()
                if delete_user:
                    db.delete(delete_user)
                    db.commit()
                    return True

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

    async def updateById(self, id, payload):
        try:
            with get_db() as db:

                if payload.get('hashed_password'):
                    payload['hashed_password'] = bcrypt_context.hash(payload.get('hashed_password'))
                # 透過條件來更新
                db.query(User).filter(User.id == id).update(payload)
                db.commit()

                return True

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