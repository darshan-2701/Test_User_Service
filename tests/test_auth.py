def test_register(client):
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post('/register', json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login(client):
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    r1 = client.post("/register", json=payload)

    response = client.post('/login', json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()