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


def test_rejects_non_positive_amount(client, auth):
    res = client.post("/api/transactions", headers=auth,
                      json={"type": "expense", "amount": 0, "categoryId": "food", "date": "2026-08-10"})
    assert res.status_code == 422


def test_update_and_delete(client, auth):
    tx = make(client, auth)
    upd = client.patch(f"/api/transactions/{tx['id']}", headers=auth, json={"amount": 99, "recurring": True})
    assert upd.json()["amount"] == 99 and upd.json()["recurring"] is True
    assert client.delete(f"/api/transactions/{tx['id']}", headers=auth).status_code == 204
    assert client.get(f"/api/transactions/{tx['id']}", headers=auth).status_code == 404


def test_filters_search_and_sort(client, auth):
    make(client, auth, amount=5, note="Coffee", date="2026-08-01")
    make(client, auth, amount=50, categoryId="shopping", note="Books", date="2026-08-15")
    make(client, auth, type="income", amount=1000, categoryId="salary", note="Pay", date="2026-08-20")

    def ids(**params):
        return client.get("/api/transactions", headers=auth, params=params).json()

    assert ids(type="income")["total"] == 1
    assert ids(categoryId="shopping")["items"][0]["note"] == "Books"
    assert ids(q="coff")["total"] == 1
    assert ids(q="food & dining")["total"] == 1
    assert ids(**{"from": "2026-08-10", "to": "2026-08-16"})["total"] == 1
    assert [t["amount"] for t in ids(sort="amount-asc")["items"]] == [5, 50, 1000]
