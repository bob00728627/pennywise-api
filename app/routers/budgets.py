from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ids import new_id
from app.database import get_db
from app.models import Budget, Category, Transaction, User
from app.schemas.budget import BudgetIn, BudgetOut, BudgetStatus
from app.services.dates import days_left_in_month, month_bounds, month_key
from app.services.stats import spent_by_category

router = APIRouter(prefix="/api/budgets", tags=["budgets"])


def _status(pct: float) -> str:
    return "over" if pct >= 100 else "warn" if pct >= 80 else "ok"


def _check_category(db: Session, user: User, category_id: str) -> None:
    cat = db.get(Category, (category_id, user.id))
    if not cat or cat.type != "expense":
        raise HTTPException(422, "Budgets need an expense category")


@router.get("", response_model=list[BudgetStatus])
def list_budgets(month: str | None = None, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)) -> list[BudgetStatus]:
    key = month or month_key(date.today())
    start, end = month_bounds(key)
    txs = db.scalars(select(Transaction).where(Transaction.user_id == user.id,
                                               Transaction.date >= start, Transaction.date <= end))
    spent = spent_by_category(txs)
    days = max(1, days_left_in_month()) if key == month_key(date.today()) else 1
    out = []
    for b in db.scalars(select(Budget).where(Budget.user_id == user.id)):
        s = spent.get(b.category_id, 0.0)
        pct = round(s / b.limit * 100, 1)
        remaining = round(b.limit - s, 2)
        out.append(BudgetStatus(id=b.id, category_id=b.category_id, limit=b.limit, spent=s, remaining=remaining,
                                percent=pct, status=_status(pct),
                                per_day_left=round(max(0.0, remaining) / days, 2)))
    return out


@router.put("", response_model=BudgetOut)
def upsert_budget(body: BudgetIn, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)) -> Budget:
    """Create or replace the budget for a category (one budget per category)."""
    _check_category(db, user, body.category_id)
    budget = db.scalar(select(Budget).where(Budget.user_id == user.id, Budget.category_id == body.category_id))
    if budget:
        budget.limit = body.limit
    else:
        budget = Budget(id=new_id(), user_id=user.id, category_id=body.category_id, limit=body.limit)
        db.add(budget)
    db.commit()
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: str, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)) -> Response:
    b = db.get(Budget, budget_id)
    if not b or b.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Budget not found")
    db.delete(b)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
