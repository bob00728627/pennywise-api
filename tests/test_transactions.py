from tests.conftest import register


def make(client, auth, **kw):
    body = {"type": "expense", "amount": 10, "categoryId": "food", "note": "Lunch", "date": "2026-08-10"} | kw
    res = client.post("/api/transactions", headers=auth, json=body)
    assert res.status_code == 201, res.text
    return res.json()


def test_create_and_get(client, auth):
    tx = make(client, auth, amount=12.345)
    assert tx["amount"] == 12.35
    assert client.get(f"/api/transactions/{tx['id']}", headers=auth).json()["note"] == "Lunch"


def test_rejects_wrong_category_type(client, auth):
    res = client.post("/api/transactions", headers=auth,
                      json={"type": "income", "amount": 10, "categoryId": "food", "date": "2026-08-10"})
    assert res.status_code == 422
