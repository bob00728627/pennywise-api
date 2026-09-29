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
