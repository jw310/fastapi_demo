from fastapi.testclient import TestClient
from fastapi import status
import uuid
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from llm.database import Base, get_db
from llm.main import app
from llm.models.user import User
from llm.models.todos import Todos
from llm.utils.auth import get_current_user, bcrypt_context

# 建立測試資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# 建立 test db 的 dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 建立 test user 的 dependency
def override_get_current_user():
    return {'username': 'test', 'id': 1, 'user_role': 'admin'}

# 覆寫 db 和 user 的 原本 dependency
# app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = override_get_current_user

# 建立 client 端測試
client = TestClient(app)

# 建立 test api 的 fixture ，可以使用此物件。建立可重用性
###
# scope：表示作用域，預設為 "function"，亦即每個有用到此 fixture 的 test case 都會執行，另外還有 module、class 以及 session 三種
# name：用來設定 fixture 的別名，預設為函式名稱
# autouse：預設為 False，若為 True，則會自動進行使用 (根據 scope 作用域而定)
###
@pytest.fixture(name="test_user", scope="function", autouse=False)
def test_user():
    user = User(
        uuid=str(uuid.uuid4()),
        username='test',
        email='test@test.com',
        first_name='test',
        last_name='test',
        hashed_password=bcrypt_context.hash('test'),
        is_active=True,
        role='admin',
        phone_number='0912345678'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    # 測試後刪除
    db.close()
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

@pytest.fixture
def test_todo():
    todo = Todos(title='test', description='test', priority=1, complete=False, owner_id=1)

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture(scope="function", autouse=True)
def cleanup_database():
    """每次測試前後都清理資料庫"""
    yield
    # 測試後清理所有資料表
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()