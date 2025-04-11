from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from llm.utils.auth import get_current_user
from llm.utils.newHTTPException import NewHTTPException

from llm.models.users import (Users)

from llm.utils.auth import authenticate_user

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter()

# 建立 user 的 dependency，從 get_current_user 取得 user info
user_dependency = Annotated[dict, Depends(get_current_user)]

# 建立模板
templates = Jinja2Templates(directory="llm/templates")

#################
### Pages ###
#################


#################
### Endpoints ###
#################
@router.get("/allUsers", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException (
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
        )

    users = await Users.get_users()

    if users is None:
        raise NewHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Success",
        "users": users
    }


