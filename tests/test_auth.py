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
