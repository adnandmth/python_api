"""
https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest

Fixtures are a potential and common use of conftest.py. The fixtures that you will define will be shared among all tests in your test suite
"""
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command

"""
Provision a new database connection that is separate from the production db.
"""
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
pytest Fixture Scope Levels
Fixture scopes in Pytest control the lifetime of fixtures. They define how often a fixture gets created and destroyed.

Pytest provides four levels of fixture scopes:

Function (Set up and torn down once for each test function)
Class (Set up and torn down once for each test class)
Module (Set up and torn down once for each test module/file)
Session (Set up and torn down once for each test session i.e comprising one or more test files)
"""
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal() # get the connected DB
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session # yield a database connection from the yield db on session class
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # Create a TestClient by passing your FastAPI application (app) to it.
    
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "adnan.zahry3@gmail.com",
        "password": "password123"
    }
    res = client.post("/user/", json=user_data)
    
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user