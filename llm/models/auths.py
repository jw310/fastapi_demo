import logging
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status

# 建立 Database Table
from ..database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 驗證 Request
from pydantic import BaseModel


from llm.utils.newHTTPException import NewHTTPException

####################
# DB MODEL
####################



####################
# Request、Forms
####################

class Token(BaseModel):
    access_token: str
    token_type: str

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]


class AuthTable:
    async def get_access_token(self, form_data):
        pass




Auths = AuthTable()



