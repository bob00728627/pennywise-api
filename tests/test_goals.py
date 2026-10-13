from datetime import date, timedelta


def new_goal(client, auth, **kw):
    deadline = (date.today() + timedelta(days=90)).isoformat()
    body = {"name": "Trip", "target": 1000, "saved": 100, "deadline": deadline, "color": "#22c55e"} | kw
    res = client.post("/api/goals", headers=auth, json=body)
    assert res.status_code == 201, res.text
    return res.json()


def test_create_goal_computes_progress(client, auth):
    g = new_goal(client, auth)
    assert g["percent"] == 10 and not g["completed"]
    assert g["daysLeft"] == 90 and g["monthlyNeeded"] == 300


def test_deposit_and_withdraw(client, auth):
    g = new_goal(client, auth)
    g = client.post(f"/api/goals/{g['id']}/deposit", headers=auth, json={"amount": 900}).json()
    assert g["completed"] is True
    g = client.post(f"/api/goals/{g['id']}/deposit", headers=auth, json={"amount": -5000}).json()
    assert g["saved"] == 0
