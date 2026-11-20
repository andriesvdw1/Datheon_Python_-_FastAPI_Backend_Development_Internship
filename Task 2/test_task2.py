import pytest
from fastapi.testclient import TestClient
from task2 import app, memory_users_db

# pytest fixtures
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
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    print(f"\n[TEST] Registering user with payload: {payload}")
    
    response = client.post("/register", json=payload)
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registration successful"
    assert data["email"] == "test@example.com"


def test_register_user_already_exists(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    
    print(f"\n[TEST] Registering initial user: {payload}")
    client.post("/register", json=payload)
    
    print(f"[TEST] Attempting duplicate registration with same payload: {payload}")
    response = client.post("/register", json=payload)
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use for a user"


def test_login_success(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    client.post("/register", json=payload)
    
    form_data = {"username": "test@example.com", "password": "strongpassword123"}
    print(f"\n[TEST] Logging in user with credentials: {form_data}")
    
    response = client.post("/login", data=form_data)
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    client.post("/register", json=payload)
    
    # Wrong password test
    bad_password_data = {"username": "test@example.com", "password": "wrongpassword"}
    print(f"\n[TEST] Logging in with wrong password: {bad_password_data}")
    response = client.post("/login", data=bad_password_data)
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "email or password is invalid"

    # Non-existent user test
    non_existent_data = {"username": "nonexistent@example.com", "password": "strongpassword123"}
    print(f"\n[TEST] Logging in with non-existent user: {non_existent_data}")
    response = client.post("/login", data=non_existent_data)
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 401


def test_read_users_me_success(client):
    payload = {"email": "test@example.com", "password": "strongpassword123"}
    client.post("/register", json=payload)
    
    login_response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "strongpassword123"}
    )
    token = login_response.json()["access_token"]
    print(f"\n[TEST] Accessing protected route /users/me with token acquired for: {payload['email']}")
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"-> Response Status: {response.status_code}")
    print(f"-> Response Body: {response.json()}")
    
    assert response.status_code == 200
    assert response.json() == {"email": "test@example.com"}


def test_read_users_me_unauthorized(client):
    print(f"\n[TEST] Accessing protected route /users/me without any token")
    response = client.get("/users/me")
    print(f"-> Response Status: {response.status_code}")
    assert response.status_code == 401

    print(f"\n[TEST] Accessing protected route /users/me with invalid/malformed token")
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    print(f"-> Response Status: {response.status_code}")
    assert response.status_code == 401
