from datetime import date

from app.models import Category, Transaction
from app.services.dates import last_n_months, month_bounds
from app.services.stats import build_report, pct_change, savings_rate, spent_by_category, summary


def tx(kind, amount, cat, d):
    return Transaction(id=f"{cat}{amount}", user_id=1, type=kind, amount=amount, category_id=cat, note="", date=d)


def test_last_n_months_wraps_year():
    assert last_n_months(3, date(2026, 1, 15)) == ["2025-11", "2025-12", "2026-01"]


def test_month_bounds_leap_year():
    assert month_bounds("2028-02") == (date(2028, 2, 1), date(2028, 2, 29))


def test_savings_rate_and_change():
    assert savings_rate(0, 50) == 0
    assert savings_rate(1000, 250) == 75
    assert savings_rate(100, 500) == 0
    assert pct_change(110, 100) == 10
    assert pct_change(5, 0) is None


def test_summary_and_report():
    today = date(2026, 9, 20)
    txs = [
        tx("income", 1000, "salary", date(2026, 9, 1)),
        tx("expense", 200, "food", date(2026, 9, 3)),
        tx("income", 800, "salary", date(2026, 8, 1)),
        tx("expense", 100, "food", date(2026, 8, 3)),
        tx("expense", 350, "fun", date(2026, 8, 9)),
    ]
    s = summary(txs, today)
    assert s.balance == 1150 and s.month_income == 1000 and s.savings_rate == 80
    assert s.income_change == 25 and s.expense_change == -55.6
    cats = [Category(id="food", user_id=1, name="Food", icon="x", color="#000000", type="expense")]
    r = build_report(txs, cats, 3, today)
    assert [m.month for m in r.monthly] == ["2026-07", "2026-08", "2026-09"]
    assert r.by_category[0].category_id == "fun" and r.by_category[0].name == "Unknown"
    assert spent_by_category(txs) == {"food": 300, "fun": 350}
