def test_defaults_created_on_register(client, auth):
    res = client.get("/api/categories", headers=auth)
    assert len(res.json()) == 10
    income = client.get("/api/categories", params={"type": "income"}, headers=auth).json()
    assert {c["id"] for c in income} == {"salary", "freelance", "investments"}


def test_create_update_delete_category(client, auth):
    res = client.post("/api/categories", headers=auth,
                      json={"name": "Pets", "icon": "🐶", "color": "#123456", "type": "expense"})
    assert res.status_code == 201
    cid = res.json()["id"]
    upd = client.patch(f"/api/categories/{cid}", headers=auth, json={"name": "Pet care"})
    assert upd.json()["name"] == "Pet care"
    assert client.delete(f"/api/categories/{cid}", headers=auth).status_code == 204


def test_invalid_color(client, auth):
    body = {"name": "X", "icon": "x", "color": "red", "type": "expense"}
    res = client.post("/api/categories", headers=auth, json=body)
    assert res.status_code == 422


def test_cannot_delete_used_category(client, auth):
    client.post("/api/transactions", headers=auth,
                json={"type": "expense", "amount": 5, "categoryId": "food", "date": "2026-08-03"})
    assert client.delete("/api/categories/food", headers=auth).status_code == 409


def test_categories_are_per_user(client, auth):
    from tests.conftest import register

    other = register(client, "other@example.com")
    client.post("/api/categories", headers=auth,
                json={"id": "pets", "name": "Pets", "icon": "🐶", "color": "#123456", "type": "expense"})
    assert client.patch("/api/categories/pets", headers=other, json={"name": "x"}).status_code == 404
