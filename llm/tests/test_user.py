from fastapi import status, HTTPException
import pytest

from llm.tests.utils import app, client, override_get_db, override_get_current_user, test_user
from llm.database import get_db
from llm.utils.auth import get_current_user

# 確保 dependency overrides 已設定
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# def test_dependency_override_works():
#     # check override is set
#     assert get_db in app.dependency_overrides
#     assert get_current_user in app.dependency_overrides

#     response = client.get('/api/v1/user/all')

#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

# 不驗證加密後的密碼屬性
def test_return_user_authenticated(test_user: test_user):
    print(f"test_user ID: {test_user.id}")
    print(f"test_user Username: {test_user.username}")

    response = client.get(f'/api/v1/user/{test_user.id}')
    print(f"response status code: {response.status_code}")
    print(f"response content: {response.json()}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['username'] == test_user.username

# def test_return_user_by_username_authenticated(test_user):
#     response = client.get('/api/v1/user/username', params={'username': test_user.username})
#     print(f"test_user Username: {test_user.username}")

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()['data']['username'] == test_user.username

# def test_change_phone_number_authenticated(test_user):
#     request_data = {
#         'phone_number': '0911111116'
#     }
#     response = client.patch(f'/api/v1/user/{test_user.id}', json=request_data)

#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_delete_user_by_id_authenticated(test_user):
#     response = client.delete(f'/api/v1/user/{test_user.id}')

#     assert response.status_code == status.HTTP_200_OK