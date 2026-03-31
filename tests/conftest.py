import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db) -> User:
    user = User(
        email="testuser@optimus.com",
        hashed_password=get_password_hash("Passw0rd!"),
        first_name="Test",
        last_name="User",
        phone="+521234567890",
        age=25,
        weight=75.0,
        height=175.0,
        exercise_frequency="3x/week",
        training_type="gimnasio",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def auth_headers(client, test_user) -> dict:
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@optimus.com", "password": "Passw0rd!"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
