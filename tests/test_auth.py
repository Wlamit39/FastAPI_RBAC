def test_register_user(client):
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "role": "user"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "user"

def test_register_existing_user(client):
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "role": "user"
    })
    assert response.status_code == 400

def test_login_user(client):
    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "testpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
