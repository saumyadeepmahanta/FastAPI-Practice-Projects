from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
import pytest
from ..models import Todos,Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the testing session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Override the get_current_user dependency to return a mock user
def override_get_current_user():
    return {"username": "codingwithroby", "id": 1, "user_role": "admin"}



# Create a test client
client = TestClient(app)

@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    # Clean up the database after the test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()




@pytest.fixture
def test_user():
    user=Users(
        username="codingwithroby",
        email="codingwithroby@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="Admin",
        phone_number="1123444331"
    )
    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
        
