from collections import defaultdict
from collections.abc import Iterable
from datetime import date

from app.models import Category, Transaction
from app.schemas.report import CategoryTotal, MonthRow, Report, Summary
from app.services.dates import last_n_months, month_key


def total(txs: Iterable[Transaction], kind: str) -> float:
    return round(sum(t.amount for t in txs if t.type == kind), 2)
