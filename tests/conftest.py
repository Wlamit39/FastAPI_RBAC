import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db.database import get_session

# ✅ Use a persistent SQLite file for testing
TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Override the session dependency
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # ✅ Create tables before running tests
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
    try:
        os.remove("test_db.sqlite")
    except FileNotFoundError:
        pass

@pytest.fixture
def client():
    return TestClient(app)
