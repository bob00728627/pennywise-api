import math
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ids import new_id
from app.database import get_db
from app.models import Category, Transaction, User
from app.schemas.common import Page
from app.schemas.transaction import (
    BulkDelete,
    BulkResult,
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
)
from app.services.csv_export import transactions_to_csv

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

SortKey = Literal["date-desc", "date-asc", "amount-desc", "amount-asc"]


def _ensure_category(db: Session, user: User, category_id: str, kind: str) -> None:
    cat = db.get(Category, (category_id, user.id))
    if not cat:
        raise HTTPException(422, "Unknown category")
    if cat.type != kind:
        raise HTTPException(422, f"Category '{cat.name}' is for {cat.type}")


def _get(db: Session, user: User, tx_id: str) -> Transaction:
    tx = db.get(Transaction, tx_id)
    if not tx or tx.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Transaction not found")
    return tx
