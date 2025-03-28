import logging
import uuid
from typing import Optional

# 建立 Database Table
from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# 驗證 Request
from pydantic import BaseModel

# log = logging.getLogger(__name__)
# log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################

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


####################
# Request、Forms
####################