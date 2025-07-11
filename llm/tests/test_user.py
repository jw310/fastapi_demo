from fastapi import status, HTTPException
import pytest

from llm.tests.utils import client, test_user

# 不驗證加密後的密碼屬性
def test_return_user_authenticated(test_user: test_user):
    print(f"test_user ID: {test_user.id}")
    print(f"test_user Username: {test_user.username}")

    response = client.get(f'/api/v1/user/{test_user.id}')
    print(f"response status code: {response.status_code}")
    print(f"response content: {response.json()}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['username'] == test_user.username

def test_return_user_by_username_authenticated(test_user):
    response = client.get('/api/v1/user/username', params={'username': test_user.username})
    print(f"test_user Username: {test_user.username}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['username'] == test_user.username

def test_change_phone_number_authenticated(test_user):
    request_data = {
        'phone_number': '0911111116'
    }
    response = client.patch(f'/api/v1/user/{test_user.id}', json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_user_by_id_authenticated(test_user):
    response = client.delete(f'/api/v1/user/{test_user.id}')

    assert response.status_code == status.HTTP_200_OK