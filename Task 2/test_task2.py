import pytest
from fastapi.testclient import TestClient
from main import app, memory_users_db

# pytest tests to verify task2 user registration, login and token authentication
@pytest.fixture(autouse=True)
def clear_db():
    """Clear the in-memory user database before each test."""
    memory_users_db.clear()
    yield
    memory_users_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_register_user_success(client):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registration successful"
    assert data["email"] == "test@example.com"


def test_register_user_already_exists(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    
    # Register the first time
    client.post("/register", json=payload)
    
    # Try registering again with the same email
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use for a user"


def test_login_success(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    
    # Register user first
    client.post("/register", json=payload)
    
    # OAuth2PasswordRequestForm expects form data with 'username' and 'password'
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    client.post("/register", json=payload)
    
    # Wrong password
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "email or password is invalid"

    # Non-existent user
    response = client.post(
        "/login",
        data={"username": "nonexistent@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 401


def test_read_users_me_success(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    client.post("/register", json=payload)
    
    # Login to get the access token
    login_response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "strongpassword123"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected route with Bearer token
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"email": "test@example.com"}


def test_read_users_me_unauthorized(client):
    # Try accessing without a token
    response = client.get("/users/me")
    assert response.status_code == 401

    # Try accessing with a malformed/invalid token
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    assert response.status_code == 401
