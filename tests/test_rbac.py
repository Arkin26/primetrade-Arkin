def test_user_cannot_access_other_users_task(client, user_headers):
    other = client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "password": "password123"},
    ).json()
    other_headers = {"Authorization": f"Bearer {other['access_token']}"}

    task = client.post(
        "/api/v1/tasks",
        headers=other_headers,
        json={"title": "Private task"},
    ).json()

    response = client.get(f"/api/v1/tasks/{task['id']}", headers=user_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_admin_can_access_any_task(client, admin_headers, user_headers):
    task = client.post(
        "/api/v1/tasks",
        headers=user_headers,
        json={"title": "User task"},
    ).json()

    response = client.get(f"/api/v1/tasks/{task['id']}", headers=admin_headers)
    assert response.status_code == 200


def test_admin_can_list_all_tasks(client, admin_headers, user_headers):
    client.post("/api/v1/tasks", headers=user_headers, json={"title": "Task A"})
    client.post("/api/v1/tasks", headers=user_headers, json={"title": "Task B"})

    response = client.get("/api/v1/tasks", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["total"] >= 2


def test_non_admin_cannot_list_users(client, user_headers):
    response = client.get("/api/v1/users", headers=user_headers)
    assert response.status_code == 403


def test_admin_can_list_users(client, admin_headers):
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_admin_can_update_user_role(client, admin_headers, registered_user):
    user_id = registered_user["user"]["id"]
    response = client.patch(
        f"/api/v1/users/{user_id}/role",
        headers=admin_headers,
        json={"role": "admin"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"
