import warnings
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base, get_db
from db import models
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # or use ":memory:" for in-memory DB
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Provides a database session for testing purposes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create tables in the test database before running tests"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

admin_token = None  # Global variable to store admin token # pylint: disable=C0103

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="'crypt' is deprecated and slated for removal in Python 3.13"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version"
)

def test_create_user_a():
    """Tests creating a new user (User A)."""
    response = client.post(
        "/users/",
        json={
            "username": "userA",
            "email": "userA@example.com",
            "password": "Password123!"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "userA@example.com"
    assert "password" not in data

def test_create_user_b_and_upgrade_to_admin():
    """Tests creating a new user (User B) and upgrading them to admin."""
    global admin_token # pylint: disable=W0602,W0603

    response = client.post(
        "/users/",
        json={
            "username": "userB",
            "email": "userB@example.com",
            "password": "Password123!"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "userB@example.com"

    # Manually upgrade User B to admin in the test database
    db = next(override_get_db())
    user_b = db.query(models.User).filter_by(email="userB@example.com").first()
    user_b.role = "admin"
    db.commit()

    # Authenticate as User B to get an access token
    response = client.post(
        "/auth/login",
        json={"username": "userB@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    tokens = response.json()
    admin_token = tokens["access_token"]

def test_user_a_edits_own_username():
    """Tests that User A can edit their own username."""

    response = client.post(
        "/auth/login",
        json={"username": "userA@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    tokens = response.json()
    user_a_token = tokens["access_token"]

    # Get User A's ID
    db = next(override_get_db())
    user_a = db.query(models.User).filter_by(email="userA@example.com").first()
    user_a_id = user_a.id

    # User A updates their own username
    response = client.put(
        f"/users/{user_a_id}",
        json={"username": "new_username.png"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "new_username.png"

def test_user_a_attempts_admin_rights():
    """Tests that User A cannot grant themselves admin privileges."""
    response = client.post(
        "/auth/login",
        json={"username": "userA@example.com", "password": "Password123!"},
    )
    tokens = response.json()
    user_a_token = tokens["access_token"]

    db = next(override_get_db())
    user_a = db.query(models.User).filter_by(email="userA@example.com").first()
    user_a_id = user_a.id

    response = client.put(
        f"/users/{user_a_id}/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response.status_code == 403  # Forbidden
    data = response.json()
    assert data["detail"] == "Admin privileges required"

def test_user_a_attempts_to_edit_user_b():
    """Tests that User A cannot edit User B's username."""

    response = client.post(
        "/auth/login",
        json={"username": "userA@example.com", "password": "Password123!"},
    )
    tokens = response.json()
    user_a_token = tokens["access_token"]

    db = next(override_get_db())
    user_b = db.query(models.User).filter_by(email="userB@example.com").first()
    user_b_id = user_b.id

    response = client.put(
        f"/users/{user_b_id}",
        json={"username": "malicious_username.png"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response.status_code == 403  # Forbidden
    data = response.json()
    assert data["detail"] == "Operation not permitted"

def test_admin_user_b_gives_admin_rights_to_user_a():
    """Tests that User B (admin) can grant admin privileges to User A."""
    global admin_token # pylint: disable=W0602

    db = next(override_get_db())
    user_a = db.query(models.User).filter_by(email="userA@example.com").first()
    user_a_id = user_a.id

    response = client.put(
        f"/users/{user_a_id}/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "admin"

def test_admin_user_b_deletes_users():
    """Tests that User B (admin) can delete both User A and themselves."""
    global admin_token # pylint: disable=W0602

    db = next(override_get_db())
    user_a = db.query(models.User).filter_by(email="userA@example.com").first()
    user_a_id = user_a.id

    response = client.delete(
        f"/users/{user_a_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204  # Assuming first deletion returns details

    # User B deletes themselves
    user_b = db.query(models.User).filter_by(email="userB@example.com").first()
    user_b_id = user_b.id

    response = client.delete(
        f"/users/{user_b_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204  # No content, no body to parse
