from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
# from fastapi.security import OAuth2PasswordRequestForm

from ..database import (get_db)
# 建立 Session 對話
from sqlalchemy.orm import Session

from llm.utils.auth import login_form, oauth2_bearer, authenticate_user, create_access_token, create_token_pair, verify_refresh_token

from llm.models.auths import (TokenResponse, RefreshRequest)

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter()

# 透過 Depends 注入 db，建立 Session
# 一個 db 的 dependency，可以看做是要操作的 db，這裡的 Depends 對應 get_db， get_db 對應 SessionLocal
db_dependency = Annotated[Session, Depends(get_db)]

# 建立模板
templates = Jinja2Templates(directory="llm/templates")

#################
### Pages ###
#################


#################
### Endpoints ###
#################
@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
        form_data: login_form,
        # db: db_dependency
    ):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    token = await create_token_pair(user.username, user.id, user.role)

    return {
        'access_token': token['access_token'],
        'refresh_token': token['refresh_token'],
        'token_type': token['token_type'],
    }

@router.post("/refresh")
async def refresh_for_access_token(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Refresh token with the following information:

    - **token** in `Authorization` header

    """

    print(token)
    # if not token:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    # payload = await verify_refresh_token(refresh_request)
    # print(payload)

    return {
        'a': 'a'
        # 'access_token': token['access_token'],
        # 'refresh_token': token['refresh_token'],
        # 'token_type': token['token_type'],
    }