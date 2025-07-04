import logging
from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from llm.utils.auth import get_current_user
from llm.utils.newHTTPException import NewHTTPException

from llm.models.user import (Users, CreateUserRequest)

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
async def create_user(user: user_dependency, create_user_request: CreateUserRequest):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = await Users.insert(create_user_request)

    if user:
        return {
            "message": "Success",
        }

@router.get("/username", status_code=status.HTTP_200_OK)
async def get_user_by_username(user: user_dependency, username: str):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.findByName(username)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "data": userData
    }

@router.get("/id", status_code=status.HTTP_200_OK)
async def get_user_by_id(user: user_dependency, id: int):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.findById(id)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "data": userData
    }

@router.delete("/id", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user: user_dependency, uuid: str):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.deleteById(uuid)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
    }

@router.patch("/id", status_code=status.HTTP_200_OK)
async def update_user_by_id(user: user_dependency, id: int, payload: dict = {}):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    userData = await Users.updateById(id, payload)

    if userData is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if userData:
        return {
            "message": "Success",
        }