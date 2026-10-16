def test_summary_on_demo_data(client, demo_auth):
    s = client.get("/api/reports/summary", headers=demo_auth).json()
    assert s["transactionCount"] > 50
    assert s["monthIncome"] >= 4200


def test_report_ranges(client, demo_auth):
    for months in (3, 6, 12):
        r = client.get("/api/reports", headers=demo_auth, params={"months": months}).json()
        assert len(r["monthly"]) == months
        assert abs(sum(c["percent"] for c in r["byCategory"]) - 100) < 1
    assert client.get("/api/reports", headers=demo_auth, params={"months": 5}).status_code == 422
