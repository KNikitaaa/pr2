import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import database, metadata
from models import users

# Настройка тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def test_db():
    # Создаем тестовую базу данных
    engine = create_engine(TEST_DATABASE_URL)
    metadata.create_all(engine)
    yield
    # Удаляем таблицы после завершения тестов
    metadata.drop_all(engine)

@pytest.fixture(scope="module")
def client(test_db):
    # Подключаемся к тестовой базе данных
    database._database = TEST_DATABASE_URL
    with TestClient(app) as client:
        yield client

def test_create_user(client):
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"

def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)