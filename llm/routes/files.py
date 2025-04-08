from typing import Annotated
from datetime import timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

# 建立 Session 對話
from sqlalchemy.orm import Session

from llm.utils.auth import authenticate_user, create_access_token, bcrypt_context

from llm.models.users import (Users, CreateUserRequest)

# 模板
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


output_folder = os.path.join(os.getcwd(), 'llm/data/uploadFiles')


#################
### Pages ###
#################



#################
### Endpoints ###
#################
@router.post("/create")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_files(files: list[UploadFile] | None = None, tag: str = Form()):
    if files is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
    for file in files:
        # with 關鍵字的區塊結束之後自動關閉檔案，file.close()可省略
        with open(f'{output_folder}/{file.filename}', 'wb') as f:
            # read file
            content = await file.read()
            f.write(content)

    return { "message": "File uploaded successfully",
        "files": [
            {
                "filename": file.filename,
                "file_size": file.size,
                "content_type": file.content_type,
                "tag": tag
            } for file in files
        ]
      }