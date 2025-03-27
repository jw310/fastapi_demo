from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import SessionLocal
# 建立 Session 對話
from sqlalchemy.orm import Session
from ..models import Users

from llm.utils.auth import authenticate_user, create_access_token, bcrypt_context

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# send request 之前只執行 yield 之前的程式碼
# 發送之後執行 yield 之後的程式碼
def get_db():
    # 資料庫建立一個本機 session，跟資料庫連線
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 建立模板
templates = Jinja2Templates(directory="llm/templates")

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

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


### Endpoints ###
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
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

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
    ):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

