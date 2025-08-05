from typing import Annotated
from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException
from starlette import status

# 加密
from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from ..database import (get_db)
# 建立 Session 對話
from sqlalchemy.orm import Session

# 使用 bcrypt 加密密碼
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 驗證 token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

from llm.models.user import Users

from llm.env import (SECRET_KEY, ALGORITHM)


# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 身分驗證
async def authenticate_user(username: str, password: str):
    # user = db.query(Users).filter(Users.username == username).first()
    user = await Users.findByName(username)
    if not user:
        return False
    # bcrypt 會自動將 password 加密後比對
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def get_http_authorization_cred(auth_header: str):
    try:
        scheme, credentials = auth_header.split(" ")
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
    except Exception:
        raise ValueError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# 建立 JWT token
async def create_access_token(username: str, id: int, role: str, expires_delta: timedelta):
    encode = {
        # sub 通常是指使用者的 id
        "sub": str(id),
        "name": username,
        "role": role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# 解碼 JWT 取得當前使用者
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("name")
        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")

        token_is_expired = await get_token_remaining_time(token)
        print(token_is_expired)

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return { 'username': username, 'id': user_id, 'user_role': user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Invalid authentication credentials")

# check token expired
async def check_token_expired(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        now = datetime.now()
        now_timestamp = int(now.timestamp())
        expires = payload.get("exp")

        if expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return now_timestamp > expires
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Invalid authentication credentials")

async def get_token_remaining_time(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        now = datetime.now()
        expires = payload.get("exp")
        now1 = now.strftime("%Y-%m-%d %H:%M:%S")
        expires1 = datetime.fromtimestamp(expires)

        print("Now:", now1)
        print("Expires1:", expires1)

        # remaining_time = now1 - expires1

        # if expires is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        # return remaining_time
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Invalid authentication credentials")

# refresh token