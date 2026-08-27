from app.schemas.base import CamelModel


class MonthRow(CamelModel):
    month: str
    income: float
    expense: float
    net: float


class CategoryTotal(CamelModel):
    category_id: str
    name: str
    color: str
    total: float
    percent: float


class Summary(CamelModel):
    balance: float
    month_income: float
    month_expense: float
    savings_rate: float
    income_change: float | None
    expense_change: float | None
    transaction_count: int


class Report(CamelModel):
    months: int
    total_income: float
    total_expense: float
    avg_monthly_expense: float
    savings_rate: float
    monthly: list[MonthRow]
    by_category: list[CategoryTotal]
