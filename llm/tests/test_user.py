from fastapi import status, HTTPException
import pytest

from llm.tests.utils import app, client, override_get_db, override_get_current_user, test_user
from llm.database import get_db
from llm.utils.auth import get_current_user

# 確保 dependency overrides 已設定
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# def test_dependency_override_works():
#     """驗證 dependency override 是否正常工作"""
#     # 檢查 override 是否已設定
#     assert get_db in app.dependency_overrides
#     assert get_current_user in app.dependency_overrides

#     # 測試 API 是否使用測試資料庫
#     response = client.get('/api/v1/user/all')
#     # 如果 override 正常工作，應該不會有認證問題
#     assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

# 不驗證加密後的密碼屬性
def test_return_user_authenticated(test_user: test_user):
    """測試通過 ID 取得用戶資料"""
    print(f"測試用戶 ID: {test_user.id}")
    print(f"測試用戶名稱: {test_user.username}")

    response = client.get(f'/api/v1/user/{test_user.id}')
    print(f"回應狀態碼: {response.status_code}")
    print(f"回應內容: {response.json()}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['username'] == test_user.username

# def test_return_user_by_username_authenticated(test_user):
#     """測試通過用戶名取得用戶資料"""
#     response = client.get('/api/v1/user/username', params={'username': test_user.username})
#     print(f"查詢用戶名: {test_user.username}")
#     print(f"回應狀態碼: {response.status_code}")
#     print(f"回應內容: {response.json()}")

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()['data']['username'] == test_user.username

# def test_change_phone_number_authenticated(test_user):
#     """測試更新用戶電話號碼"""
#     request_data = {
#         'phone_number': '0911111116'
#     }

#     response = client.patch(f'/api/v1/user/{test_user.id}', json=request_data)
#     print(f"更新用戶 ID: {test_user.id}")
#     print(f"回應狀態碼: {response.status_code}")

#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_delete_user_by_id_authenticated(test_user):
#     """測試刪除用戶"""
#     response = client.delete(f'/api/v1/user/{test_user.id}')
#     print(f"刪除用戶 ID: {test_user.id}")
#     print(f"回應狀態碼: {response.status_code}")

#     assert response.status_code == status.HTTP_200_OK