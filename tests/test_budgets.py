from datetime import date


def test_upsert_is_one_per_category(client, auth):
    a = client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 100}).json()
    b = client.put("/api/budgets", headers=auth, json={"categoryId": "food", "limit": 300}).json()
    assert a["id"] == b["id"] and b["limit"] == 300
    assert len(client.get("/api/budgets", headers=auth).json()) == 1


def test_budget_requires_expense_category(client, auth):
    assert client.put("/api/budgets", headers=auth, json={"categoryId": "salary", "limit": 10}).status_code == 422
