import httpx
from fastapi import HTTPException, status
from enum import Enum

from llm.utils.newHTTPException import NewHTTPException
from llm.env import OPENAI_API_KEY, ANTHROPIC_CLAUDE_API_KEY, GEMINI_API_KEY

# 建立 OpenAI 客戶端
async def call_openai(message: str, model: str = 'gpt-4o-mini', **kwargs):
        try:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000)
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="OpenAI API error")

                data = response.json()
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage")
                }

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

# 建立 Claude 客戶端
async def call_claude(message: str, model: str = "claude-3-sonnet-20240229", **kwargs):
        try:
            headers = {
                "x-api-key": f"{ANTHROPIC_CLAUDE_API_KEY}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": model,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "messages": [{"role": "user", "content": message}],
                "temperature": kwargs.get("temperature", 0.7)
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Claude API error")

                data = response.json()
                return {
                    "response": data["content"][0]["text"],
                    "usage": data.get("usage")
                }

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

# 建立 Gemini 客戶端
async def call_gemini(self, message: str, model: str = "gemini-pro", **kwargs):
        try:

            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
            params = {"key": f'{GEMINI_API_KEY}'}

            payload = {
                "contents": [{"parts": [{"text": message}]}],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "maxOutputTokens": kwargs.get("max_tokens", 1000)
                }
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    params=params,
                    json=payload,
                    timeout=30.0
                )

                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Gemini API error")

                data = response.json()
                return {
                    "response": data["candidates"][0]["content"]["parts"][0]["text"],
                    "usage": data.get("usageMetadata")
                }

        except Exception as e:
            raise NewHTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
                msg=str(e)
            )

