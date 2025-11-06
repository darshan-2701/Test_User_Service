import pytest
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from app.db import Base, get_db
from app.main import app
import os
test_db_path = "./test.db"

# Delete database file BEFORE test run
if os.path.exists(test_db_path):
    os.remove(test_db_path)

db_url = "sqlite:///./test.db"
engine = create_engine(url=db_url, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def reset_db():
    # Drop and recreate tables before each test for absolute isolation
    from app.db import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
