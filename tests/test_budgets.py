from datetime import date


def test_upsert_is_one_per_category(client, auth):
    a = client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 100}).json()
    b = client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 300}).json()
    assert a["id"] == b["id"] and b["limit"] == 300
    assert len(client.get("/api/budgets", headers=auth).json()) == 1


def test_budget_requires_expense_category(client, auth):
    assert client.put("/api/budgets", headers=auth, json={"categoryId": "salary", "limit": 10}).status_code == 422


def test_budget_status(client, auth):
    today = date.today().isoformat()
    client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 100})
    client.post("/api/transactions", headers=auth,
                json={"type": "expense", "amount": 85, "categoryId": "food", "date": today})
    b = client.get("/api/budgets", headers=auth).json()[0]
    assert b["spent"] == 85 and b["percent"] == 85 and b["status"] == "warn" and b["remaining"] == 15
    client.post("/api/transactions", headers=auth,
                json={"type": "expense", "amount": 30, "categoryId": "food", "date": today})
    assert client.get("/api/budgets", headers=auth).json()[0]["status"] == "over"


def test_budget_for_past_month(client, auth):
    client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 100})
    client.post("/api/transactions", headers=auth,
                json={"type": "expense", "amount": 20, "categoryId": "food", "date": "2026-01-05"})
    b = client.get("/api/budgets", headers=auth, params={"month": "2026-01"}).json()[0]
    assert b["spent"] == 20


def test_delete_budget(client, auth):
    b = client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 100}).json()
    assert client.delete(f"/api/budgets/{b['id']}", headers=auth).status_code == 204
    assert client.delete(f"/api/budgets/{b['id']}", headers=auth).status_code == 404
