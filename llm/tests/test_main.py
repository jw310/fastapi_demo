from llm.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    """驗證 API 是否正常工作"""
    response = client.get('/healthy')
    print(f"response content: {response.json()}")
    print (f"response status code: {response.status_code}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}