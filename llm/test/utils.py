from fastapi.testclient import TestClient
from fastapi import status
import uuid
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from llm.database import Base
from llm.main import app
from llm.models.user import User
from llm.models.todos import Todos
from llm.utils.auth import bcrypt_context

# 建立測試資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool
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
    return {'username': 'test', 'id': '1', 'user_role': 'admin'}

# 建立 client 端測試
client = TestClient(app)

# 建立 test api 的 fixture，測試後刪除
@pytest.fixture
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
        phone_number='09123456789'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
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
