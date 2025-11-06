def test_get_user(client):
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    # register first
    r1 = client.post("/register", json=payload)

    # Login to get a token first
    login_res = client.post("/login", json=payload)
    token = login_res.json()["access_token"]

    # Call protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/1", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == 1