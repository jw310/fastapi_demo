import logging
import uuid
from enum import Enum
from typing import Optional, Annotated, Dict, Any
from fastapi import Depends, status, HTTPException

# 建立 Database Table
from ..database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from llm.utils.newHTTPException import NewHTTPException

# 驗證 Request
from pydantic import BaseModel

class LLMProvider(str, Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"

####################
# DB MODEL
####################
# class Chats(Base):
    # __tablename__ = "chats"

    # id = Column(Integer, primary_key=True, index=True)
    # uuid = Column(String(36), unique=True, nullable=False)
    # title = Column(String, nullable=False)
    # description = Column(String, nullable=True)
    # owner_id = Column(Integer, nullable=False)

####################
# Request、Forms
####################
class CreateChatRequest(BaseModel):
    provider: LLMProvider
    user_message: str
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class CreateSystemRequest(BaseModel):
    provider: LLMProvider
    system_message: str
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class ChatResponse(BaseModel):
    provider: str
    model: str
    response: str
    usage: Optional[Dict[str, Any]] = None

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

class ChatsTable:
    async def insert(self, create_chat_request):
        try:
            # with get_db() as db:
            #     create_chat_model = Chats(
            #         uuid=str(uuid.uuid4()),
            #         title=create_chat_request.title,
            #         description=create_chat_request.description,
            #         owner_id=create_chat_request.owner_id,
            #         is_active=True
            #     )
            #     db.add(create_chat_model)
            #     db.commit()

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


# Chats = ChatsTable()
