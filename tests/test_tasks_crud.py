def test_task_crud_lifecycle(client, user_headers):
    create_response = client.post(
        "/api/v1/tasks",
        headers=user_headers,
        json={"title": "First task", "description": "Do something"},
    )
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    assert task["title"] == "First task"
    assert task["status"] == "pending"

    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=user_headers)
    assert get_response.status_code == 200

    update_response = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=user_headers,
        json={"status": "in_progress"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "in_progress"

    list_response = client.get("/api/v1/tasks", headers=user_headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=user_headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/tasks/{task_id}", headers=user_headers)
    assert missing_response.status_code == 404


def test_create_task_validation_error(client, user_headers):
    response = client.post("/api/v1/tasks", headers=user_headers, json={"title": ""})
    assert response.status_code == 422


def test_get_missing_task_returns_404(client, user_headers):
    response = client.get(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000099",
        headers=user_headers,
    )
    assert response.status_code == 404
