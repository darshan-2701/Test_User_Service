from fastapi import status


def test_register_duplicate_email(client):
    # 1) Register first time (should succeed)
    payload = {"email": "dup@example.com", "password": "Password1!"}
    r1 = client.post("/register", json=payload)
    assert r1.status_code == status.HTTP_201_CREATED

    # 2) Register same email again (should fail with 400)
    r2 = client.post("/register", json=payload)
    assert r2.status_code == status.HTTP_400_BAD_REQUEST
    data = r2.json()
    assert "Email already exists" in data.get("detail", "")

def test_register_missing_password(client):
    payload = {"email": "nopass@example.com"}
    r = client.post("/register", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_register_invalid_email_format(client):
    # Invalid email format should be rejected by Pydantic -> 422
    payload = {"email": "not-an-email", "password": "Password1!"}
    r = client.post("/register", json=payload)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_login_wrong_password(client):
    payload = {"email": "user1@example.com", "password": "RightPass123"}
    client.post("/register", json=payload)

    # Try login with wrong password -> 401 Unauthorized
    bad = {"email": "user1@example.com", "password": "WrongPassword"}
    r = client.post("/login", json=bad)
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json().get("detail") == "Invalid credentials"

def test_login_nonexistent_user(client):
    # Login attempt for an email that doesn't exist -> 401
    r = client.post("/login", json={"email": "noone@example.com", "password": "xyz"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED