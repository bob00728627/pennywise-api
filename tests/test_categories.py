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
