from typing import Annotated
from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException
from starlette import status

# encrypt
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from ..database import (get_db)
# create Session 對話
from sqlalchemy.orm import Session

# use bcrypt encrypt password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# verify token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")
login_form = Annotated[OAuth2PasswordRequestForm, Depends()]

from llm.models.user import Users

from llm.env import (
    ACCESS_TOKEN_SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM
)


# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 類型對應 SessionLocal
# Annotated 使用註釋將元資料（x）新增給類型 T： Annotated[T, x]
db_dependency = Annotated[Session, Depends(get_db)]

# authenticate user
async def authenticate_user(username: str, password: str):
    # user = db.query(Users).filter(Users.username == username).first()
    user = await Users.findByName(username)
    if not user:
        return False
    # bcrypt will automatically encrypt the password and compare it
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def get_http_authorization_cred(auth_header: str):
    try:
        scheme, credentials = auth_header.split(" ")
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
    except Exception:
        raise ValueError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# Create JWT token
async def create_access_token(username: str, id: int, role: str):
    encode = {
        # sub usually refers to the user's id
        "sub": str(id),
        "name": username,
        "role": role
    }
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(username: str, id: int, role: str):
    encode = {
        "sub": str(id),
        "name": username,
        "role": role
    }
    expires = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

async def create_token_pair(username: str, id: int, role: str):
    access_token = await create_access_token(username, id, role)
    refresh_token = await create_refresh_token(username, id, role)

    return dict(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )

# Verify token
async def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Invalid authentication credentials")


# Decode JWT to get the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
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
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
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
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        expires = datetime.fromtimestamp(payload.get("exp"))
        now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

        remaining_time = expires - now

        if expires is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return remaining_time
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Invalid authentication credentials")

# refresh token