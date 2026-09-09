from tests.conftest import register


def test_register_returns_token_and_user(client):
    res = client.post("/api/auth/register", json={"email": "A@Example.com", "name": "A", "password": "password1"})
    assert res.status_code == 201
    body = res.json()
    assert body["tokenType"] == "bearer"
    assert body["user"]["email"] == "a@example.com"


def test_duplicate_email_rejected(client):
    register(client)
    res = client.post("/api/auth/register", json={"email": "alex@example.com", "name": "B", "password": "password1"})
    assert res.status_code == 409


def test_short_password_rejected(client):
    res = client.post("/api/auth/register", json={"email": "x@example.com", "name": "X", "password": "short"})
    assert res.status_code == 422


def test_login_and_me(client):
    register(client)
    res = client.post("/api/auth/token", data={"username": "alex@example.com", "password": "supersecret"})
    assert res.status_code == 200
    token = res.json()["accessToken"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["name"] == "Alex"
