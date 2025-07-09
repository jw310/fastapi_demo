from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
# 建立 Session 對話
from sqlalchemy.orm import Session

from llm.utils.newHTTPException import NewHTTPException
from llm.utils.auth import get_current_user
from llm.models.chat import LLMProvider, CreateChatRequest, CreateSystemRequest
from llm.utils.llmClient import call_openai, call_claude, call_gemini

# 建立 user 的 dependency，從 get_current_user 取得 user info
user_dependency = Annotated[dict, Depends(get_current_user)]

# 模板
# from fastapi.templating import Jinja2Templates

router = APIRouter()

# output_folder = os.path.join(os.getcwd(), 'llm/data/uploadFiles')


#################
### Pages ###
#################


#################
### Endpoints ###
#################
@router.post("/new", status_code=status.HTTP_200_OK)
async def create_chat(user: user_dependency, request: CreateChatRequest):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    if request.provider == LLMProvider.OPENAI:
        result = await call_openai(request.user_message,
            request.model or 'gpt-4o-mini',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    elif request.provider == LLMProvider.CLAUDE:
        result = await call_claude(request.user_message,
            request.model or 'claude-3-sonnet-20240229',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    elif request.provider == LLMProvider.GEMINI:
        result = await call_gemini(request.user_message,
            request.model or 'gemini-pro',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    else:
        raise NewHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid provider")

    return {
        "message": "Success",
        "data": {
            "provider": request.provider,
            "model": request.model,
            "response": result["response"],
            "usage": result["usage"]
        }
    }

@router.post("/system", status_code=status.HTTP_200_OK)
async def create_llm_system_prompt(user: user_dependency, request: CreateSystemRequest):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    if request.provider == LLMProvider.OPENAI:
        result = await call_openai(request.system_message,
            request.model or 'gpt-4o-mini',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    elif request.provider == LLMProvider.CLAUDE:
        result = await call_claude(request.system_message,
            request.model or 'claude-3-sonnet-20240229',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    elif request.provider == LLMProvider.GEMINI:
        result = await call_gemini(request.system_message,
            request.model or 'gemini-pro',
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
    else:
        raise NewHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid provider")

    return {
        "message": "Success",
        "data": {
            "provider": request.provider,
            "model": request.model,
            "response": result["response"],
            "usage": result["usage"]
        }
    }


@router.get("/providers", status_code=status.HTTP_200_OK)
async def get_llm_providers(user: user_dependency):
    if user is None:
        raise NewHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    return {
        "message": "Success",
        "providers": [provider.value for provider in LLMProvider],
        "models": {
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o-mini"],
            "claude": ["claude-3-sonnet-20240229", "claude-3-opus-20240229"],
            "gemini": ["gemini-pro", "gemini-pro-vision"],
        }
    }