def test_projects_access(client):
    # Create admin
    client.post("/register", json={"username": "admin", "password": "adminpass", "role": "admin"})
    token_admin = client.post(
        "/login",
        data={"username": "admin", "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()["access_token"]

    # Create normal user
    client.post("/register", json={"username": "bob", "password": "bobpass", "role": "user"})
    token_user = client.post(
        "/login",
        data={"username": "bob", "password": "bobpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()["access_token"]

    # User should NOT create project
    response = client.post("/projects", json={"name": "P1", "description": "Test"}, headers={"Authorization": f"Bearer {token_user}"})
    assert response.status_code == 403

    # Admin can create project
    response = client.post("/projects", json={"name": "P1", "description": "Test"}, headers={"Authorization": f"Bearer {token_admin}"})
    assert response.status_code == 200
    project_id = response.json()["id"]

    # Both can view projects
    response = client.get("/projects", headers={"Authorization": f"Bearer {token_user}"})
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Admin can update project
    response = client.put(f"/projects/{project_id}", json={"name": "Updated", "description": "Updated"}, headers={"Authorization": f"Bearer {token_admin}"})
    assert response.status_code == 200

    # Admin can delete project
    response = client.delete(f"/projects/{project_id}", headers={"Authorization": f"Bearer {token_admin}"})
    assert response.status_code == 200
