def test_register_success(client, user_credentials):
    response = client.post("/api/v1/auth/register", json=user_credentials)
    assert response.status_code == 201
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == user_credentials["email"]
    assert data["user"]["role"] == "user"


def test_register_duplicate_email(client, user_credentials):
    client.post("/api/v1/auth/register", json=user_credentials)
    response = client.post("/api/v1/auth/register", json=user_credentials)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONFLICT"


def test_register_validation_error(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "short"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_login_success(client, registered_user, user_credentials):
    response = client.post("/api/v1/auth/login", json=user_credentials)
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_invalid_credentials(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_me_authenticated(client, user_headers, user_credentials):
    response = client.get("/api/v1/auth/me", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["email"] == user_credentials["email"]


def test_me_unauthenticated(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
