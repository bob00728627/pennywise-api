from calendar import monthrange
from datetime import date


def month_key(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def last_n_months(n: int, today: date | None = None) -> list[str]:
    today = today or date.today()
    out: list[str] = []
    y, m = today.year, today.month
    for _ in range(n):
        out.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return list(reversed(out))


def month_bounds(key: str) -> tuple[date, date]:
    y, m = map(int, key.split("-"))
    return date(y, m, 1), date(y, m, monthrange(y, m)[1])


def days_left_in_month(today: date | None = None) -> int:
    today = today or date.today()
    return monthrange(today.year, today.month)[1] - today.day
