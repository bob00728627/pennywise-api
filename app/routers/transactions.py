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


def _filtered(user: User, q: str | None, type: str | None, category_id: str | None,
              date_from: date | None, date_to: date | None) -> Select:
    stmt = select(Transaction).where(Transaction.user_id == user.id)
    if type:
        stmt = stmt.where(Transaction.type == type)
    if category_id:
        stmt = stmt.where(Transaction.category_id == category_id)
    if date_from:
        stmt = stmt.where(Transaction.date >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.date <= date_to)
    if q:
        like = f"%{q.lower()}%"
        names = select(Category.id).where(Category.user_id == user.id, func.lower(Category.name).like(like))
        stmt = stmt.where(or_(func.lower(Transaction.note).like(like), Transaction.category_id.in_(names)))
    return stmt


def _sorted(stmt: Select, sort: SortKey) -> Select:
    key, direction = sort.split("-")
    col = Transaction.date if key == "date" else Transaction.amount
    return stmt.order_by(col.asc() if direction == "asc" else col.desc(), Transaction.id)


@router.get("", response_model=Page[TransactionOut])
def list_transactions(
    q: str | None = None,
    type: Literal["income", "expense"] | None = None,
    category_id: str | None = Query(default=None, alias="categoryId"),
    date_from: date | None = Query(default=None, alias="from"),
    date_to: date | None = Query(default=None, alias="to"),
    sort: SortKey = "date-desc",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=200, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Page[TransactionOut]:
    stmt = _filtered(user, q, type, category_id, date_from, date_to)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(_sorted(stmt, sort).offset((page - 1) * page_size).limit(page_size))
    return Page(items=[TransactionOut.model_validate(r) for r in rows], total=total, page=page,
                page_size=page_size, pages=max(1, math.ceil(total / page_size)))


@router.get("/export.csv", response_class=Response)
def export_csv(
    q: str | None = None,
    type: Literal["income", "expense"] | None = None,
    category_id: str | None = Query(default=None, alias="categoryId"),
    date_from: date | None = Query(default=None, alias="from"),
    date_to: date | None = Query(default=None, alias="to"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    rows = list(db.scalars(_sorted(_filtered(user, q, type, category_id, date_from, date_to), "date-desc")))
    cats = list(db.scalars(select(Category).where(Category.user_id == user.id)))
    filename = f"pennywise-{date.today().isoformat()}.csv"
    return Response(transactions_to_csv(rows, cats), media_type="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/{tx_id}", response_model=TransactionOut)
def get_transaction(tx_id: str, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> Transaction:
    return _get(db, user, tx_id)


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(body: TransactionCreate, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)) -> Transaction:
    _ensure_category(db, user, body.category_id, body.type)
    tx = Transaction(user_id=user.id, **body.model_dump(exclude={"id"}), id=body.id or new_id())
    tx.amount = round(tx.amount, 2)
    tx.note = tx.note.strip()
    if db.get(Transaction, tx.id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Transaction id already exists")
    db.add(tx)
    db.commit()
    return tx


@router.patch("/{tx_id}", response_model=TransactionOut)
def update_transaction(tx_id: str, body: TransactionUpdate, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)) -> Transaction:
    tx = _get(db, user, tx_id)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(tx, k, v)
    _ensure_category(db, user, tx.category_id, tx.type)
    tx.amount = round(tx.amount, 2)
    db.commit()
    return tx


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(tx_id: str, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)) -> Response:
    db.delete(_get(db, user, tx_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/bulk-delete", response_model=BulkResult)
def bulk_delete(body: BulkDelete, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> BulkResult:
    count = (db.query(Transaction)
             .filter(Transaction.user_id == user.id, Transaction.id.in_(body.ids))
             .delete(synchronize_session=False))
    db.commit()
    return BulkResult(deleted=count)
