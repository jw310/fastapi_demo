from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import (get_db)
# 建立 Session 對話
from sqlalchemy.orm import Session

from llm.utils.auth import authenticate_user, create_access_token, bcrypt_context

from llm.models.users import (Users, CreateUserRequest)

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 建立模板
templates = Jinja2Templates(directory="llm/templates")

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


### Endpoints ###
@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_users():
    users = await Users.get_users()

    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "users": users
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    user = await Users.insert_new_user(create_user_request)
    # print(user)

    return {
        "message": "User created successfully",
    }

@router.get("/username", status_code=status.HTTP_200_OK)
async def get_user_by_username(username: str):
    user = await Users.get_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "user": user
    }

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    user = await Users.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "user": user
    }

