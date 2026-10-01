from collections import defaultdict
from collections.abc import Iterable
from datetime import date

from app.models import Category, Transaction
from app.schemas.report import CategoryTotal, MonthRow, Report, Summary
from app.services.dates import last_n_months, month_key


def total(txs: Iterable[Transaction], kind: str) -> float:
    return round(sum(t.amount for t in txs if t.type == kind), 2)


def savings_rate(income: float, expense: float) -> float:
    return 0.0 if income <= 0 else round(max(0.0, (income - expense) / income * 100), 1)


def pct_change(cur: float, prev: float) -> float | None:
    return None if prev == 0 else round((cur - prev) / prev * 100, 1)


def spent_by_category(txs: Iterable[Transaction]) -> dict[str, float]:
    acc: dict[str, float] = defaultdict(float)
    for t in txs:
        if t.type == "expense":
            acc[t.category_id] += t.amount
    return {k: round(v, 2) for k, v in acc.items()}


def summary(txs: list[Transaction], today: date | None = None) -> Summary:
    prev_key, cur_key = last_n_months(2, today)
    cur = [t for t in txs if month_key(t.date) == cur_key]
    prev = [t for t in txs if month_key(t.date) == prev_key]
    income, expense = total(cur, "income"), total(cur, "expense")
    return Summary(
        balance=round(total(txs, "income") - total(txs, "expense"), 2),
        month_income=income,
        month_expense=expense,
        savings_rate=savings_rate(income, expense),
        income_change=pct_change(income, total(prev, "income")),
        expense_change=pct_change(expense, total(prev, "expense")),
        transaction_count=len(txs),
    )


def build_report(txs: list[Transaction], categories: list[Category], months: int,
                 today: date | None = None) -> Report:
    keys = last_n_months(months, today)
    in_range = [t for t in txs if month_key(t.date) >= keys[0]]
    monthly = []
    for k in keys:
        m = [t for t in in_range if month_key(t.date) == k]
        inc, exp = total(m, "income"), total(m, "expense")
        monthly.append(MonthRow(month=k, income=inc, expense=exp, net=round(inc - exp, 2)))
    income, expense = total(in_range, "income"), total(in_range, "expense")
    lookup = {c.id: c for c in categories}
    by_cat = sorted(spent_by_category(in_range).items(), key=lambda kv: kv[1], reverse=True)
    return Report(
        months=months,
        total_income=income,
        total_expense=expense,
        avg_monthly_expense=round(expense / months, 2),
        savings_rate=savings_rate(income, expense),
        monthly=monthly,
        by_category=[
            CategoryTotal(
                category_id=cid,
                name=lookup[cid].name if cid in lookup else "Unknown",
                color=lookup[cid].color if cid in lookup else "#94a3b8",
                total=v,
                percent=round(v / expense * 100, 1) if expense else 0,
            )
            for cid, v in by_cat
        ],
    )
