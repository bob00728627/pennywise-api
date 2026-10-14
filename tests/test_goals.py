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


def test_zero_deposit_rejected(client, auth):
    g = new_goal(client, auth)
    assert client.post(f"/api/goals/{g['id']}/deposit", headers=auth, json={"amount": 0}).status_code == 422


def test_update_and_delete_goal(client, auth):
    g = new_goal(client, auth)
    assert client.patch(f"/api/goals/{g['id']}", headers=auth, json={"target": 200}).json()["percent"] == 50
    assert client.delete(f"/api/goals/{g['id']}", headers=auth).status_code == 204
    assert client.get("/api/goals", headers=auth).json() == []


def test_goals_sorted_by_deadline(client, auth):
    new_goal(client, auth, name="Later", deadline=(date.today() + timedelta(days=200)).isoformat())
    new_goal(client, auth, name="Sooner", deadline=(date.today() + timedelta(days=20)).isoformat())
    assert [g["name"] for g in client.get("/api/goals", headers=auth).json()] == ["Sooner", "Later"]
