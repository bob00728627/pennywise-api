from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import Category, Transaction, User
from app.schemas.report import Report, Summary
from app.services.stats import build_report, summary

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _txs(db: Session, user: User) -> list[Transaction]:
    return list(db.scalars(select(Transaction).where(Transaction.user_id == user.id)))


@router.get("/summary", response_model=Summary)
def get_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Summary:
    return summary(_txs(db, user))


@router.get("", response_model=Report)
def get_report(months: int = Query(default=6, description="3, 6 or 12"), user: User = Depends(get_current_user),
               db: Session = Depends(get_db)) -> Report:
    if months not in (3, 6, 12):
        raise HTTPException(422, "months must be 3, 6 or 12")
    cats = list(db.scalars(select(Category).where(Category.user_id == user.id)))
    return build_report(_txs(db, user), cats, months)
