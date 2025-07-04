from typing import Annotated
from datetime import timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

# 建立 Session 對話
from sqlalchemy.orm import Session

from llm.utils.newHTTPException import NewHTTPException
from llm.utils.auth import get_current_user

# from llm.models.user import (Users, CreateUserRequest)

# 建立 user 的 dependency，從 get_current_user 取得 user info
user_dependency = Annotated[dict, Depends(get_current_user)]

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter()


output_folder = os.path.join(os.getcwd(), 'llm/data/uploadFiles')


#################
### Pages ###
#################



#################
### Endpoints ###
#################
@router.post("/create")
async def create_file(user: user_dependency, file: Annotated[bytes, File()]):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return {"file_size": len(file)}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_files(user: user_dependency, files: list[UploadFile] | None = None, tag: str = Form()):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    if files is None:
        raise NewHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
    for file in files:
        # with 關鍵字的區塊結束之後自動關閉檔案，file.close()可省略
        with open(f'{output_folder}/{file.filename}', 'wb') as f:
            # read file
            content = await file.read()
            f.write(content)

    return { "message": "File uploaded successfully",
        "data": [
            {
                "filename": file.filename,
                "file_size": file.size,
                "content_type": file.content_type,
                "tag": tag
            } for file in files
        ]
      }