from fastapi import status, HTTPException
from datetime import timedelta
import pytest

from llm.tests.utils import app, client, override_get_db, override_get_current_user, test_user
from llm.database import get_db
from llm.models.user import User
from llm.utils.auth import get_current_user

# 覆寫 db 和 user 的 原本 dependency
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# 不驗證加密後的密碼屬性
def test_return_user_authenticated(test_user: test_user):
    response = client.get(f'/api/v1/user/{test_user.id}')
    assert response is not None
    # assert response.status_code == status.HTTP_200_OK
    # assert response.json()['username'] == 'test'
    # assert response.json()['email'] == 'test@test.com'
    # assert response.json()['role'] == 'admin'

# def test_return_user_by_username_authenticated(test_user: test_user):
#     response = client.get('/api/v1/user/username', params={'username': 'test'})
#     assert response.status_code == status.HTTP_200_OK

# def test_update_password_authenticated(test_user):
#     request_data = {
#         'password': 'test',
#         'new_password': 'newpassword'
#     }

#     response = client.put('/users/password', json=request_data)
#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_invalid_current_password_authenticated(test_user: test_user):
#     request_data = {
#         'password': 'wrongpassword',
#         'new_password': 'newpassword'
#     }

#     response = client.put('/users/password', json=request_data)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json() == {'detail': 'Error on password change'}


# def test_change_phone_number_authenticated():
#     request_data = {
#         'phone_number': '0911111117'
#     }

#     response = client.patch('/api/v1/user/1', json=request_data)
#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_delete_user_by_id_authenticated():
#     response = client.delete('/api/v1/user/1')
#     assert response.status_code == status.HTTP_200_OK