def test_update_settings(client, auth):
    res = client.patch("/api/settings", headers=auth, json={"currency": "JPY", "theme": "dark"})
    assert res.json()["currency"] == "JPY" and res.json()["theme"] == "dark"
    assert client.patch("/api/settings", headers=auth, json={"currency": "XXX"}).status_code == 422


def test_backup_roundtrip(client, demo_auth):
    backup = client.get("/api/backup", headers=demo_auth).json()
    assert set(backup) == {"transactions", "categories", "budgets", "goals", "settings"}
    client.post("/api/reset", headers=demo_auth, params={"demo": False})
    assert client.get("/api/transactions", headers=demo_auth).json()["total"] == 0
    restored = client.post("/api/backup", headers=demo_auth, json=backup).json()
    assert len(restored["transactions"]) == len(backup["transactions"])
    assert len(restored["goals"]) == 3


def test_reset_with_demo(client, auth):
    client.post("/api/reset", headers=auth)
    assert client.get("/api/transactions", headers=auth).json()["total"] > 0
    assert len(client.get("/api/categories", headers=auth).json()) == 10
