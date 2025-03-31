from typing import Annotated
from datetime import timedelta, datetime, timezone
import os

from fastapi import Depends, HTTPException
from starlette import status

# 加密
from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordBearer

from ..database import (get_db)
# 建立 Session 對話
from sqlalchemy.orm import Session
from ..models import Users

# 使用 bcrypt 加密密碼
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 驗證 token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

from llm.env import (SECRET_KEY, ALGORITHM)


# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 身分驗證
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    # bcrypt 會自動將 password 加密後比對
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# 建立 JWT token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# 解碼 JWT 取得當前使用者
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return { 'username': username, 'id': user_id, 'user_role': user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
