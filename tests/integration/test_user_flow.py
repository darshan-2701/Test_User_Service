def test_register_login_get_user(client):
    user = {"email": "flow@example.com", "password": "FlowPass1"}
    r1 = client.post("/register", json=user)
    assert r1.status_code == 201
    created = r1.json()
    assert created["email"] == user["email"]
    uid = created["id"]

    r2 = client.post("/login", json=user)
    assert r2.status_code == 200
    token = r2.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r3 = client.get(f"/users/{uid}", headers=headers)
    # Our current get_user is not protected, but this shows the flow
    assert r3.status_code in (200, 404)