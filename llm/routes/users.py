import logging
from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from llm.utils.auth import get_current_user
from llm.utils.newHTTPException import NewHTTPException

from llm.models.users import (Users, CreateUserRequest)

# 模板
from fastapi.templating import Jinja2Templates

from llm.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

# 建立 user 的 dependency，從 get_current_user 取得 user info
user_dependency = Annotated[dict, Depends(get_current_user)]

# 建立模板
templates = Jinja2Templates(directory="llm/templates")

#################
### Pages ###
#################
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

#################
### Endpoints ###
#################
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    user = await Users.insert_new_user(create_user_request)
    # print(user)

    return {
        "message": "User created successfully",
    }

@router.get("/username", status_code=status.HTTP_200_OK)
async def get_user_by_username(user: user_dependency, username: str):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.get_user_by_username(username)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "user": userData
    }

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user: user_dependency, user_id: int):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.get_user_by_id(user_id)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "user": userData
    }

