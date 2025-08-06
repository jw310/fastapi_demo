from fastapi import status, HTTPException
from datetime import timedelta
import pytest
from jose import jwt

# 引用 utils.py 中的所有變數、函數
from llm.tests.utils import app, override_get_db, test_user
from llm.database import get_db
from llm.utils.auth import authenticate_user, create_access_token, get_current_user
from llm.env import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

# 覆寫 db 的 原本 dependency
app.dependency_overrides[get_db] = override_get_db

# test async function, use pytest-asyncio
@pytest.mark.asyncio
async def test_authenticate_user(test_user: test_user):
    authenticated_user = await authenticate_user(test_user.username, 'test')
    assert authenticated_user is not None
    # assert authenticated_user.username == test_user.username

    non_exist_user = await authenticate_user('wrongusername', 'test')
    assert non_exist_user is False

    wrong_password_user = await authenticate_user(test_user.username, 'wrongpassword')
    assert wrong_password_user is False

@pytest.mark.asyncio
async def test_create_access_token_authenticated():
    username = 'test'
    user_id = '1'
    role = 'user'
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = await create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM], options={'verifty_signature': False})

    assert decoded_token['name'] == username
    assert decoded_token['sub'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {
        "name": "test",
        "sub": '1',
        "role": "admin"
    }

    token = jwt.encode(encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user == {'username': 'test', 'id': '1', 'user_role': 'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}

    token = jwt.encode(encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    # If an exception occurs, get HTTPException for comparison
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Invalid authentication credentials"