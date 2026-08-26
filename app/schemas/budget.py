from pydantic import Field

from app.schemas.base import CamelModel


class BudgetIn(CamelModel):
    category_id: str
    limit: float = Field(gt=0)


class BudgetOut(BudgetIn):
    id: str


class BudgetStatus(BudgetOut):
    spent: float
    remaining: float
    percent: float
    status: str
    per_day_left: float
