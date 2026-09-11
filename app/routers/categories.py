from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ids import new_id
from app.database import get_db
from app.models import Budget, Category, Transaction, User
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/api/categories", tags=["categories"])


def _get(db: Session, user: User, category_id: str) -> Category:
    cat = db.get(Category, (category_id, user.id))
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    return cat


@router.get("", response_model=list[CategoryOut])
def list_categories(type: str | None = None, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> list[Category]:
    q = select(Category).where(Category.user_id == user.id)
    if type:
        q = q.where(Category.type == type)
    return list(db.scalars(q))


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(body: CategoryCreate, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> Category:
    cid = body.id or new_id()
    if db.get(Category, (cid, user.id)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Category id already exists")
    cat = Category(user_id=user.id, **body.model_dump(exclude={"id"}), id=cid)
    db.add(cat)
    db.commit()
    return cat


@router.patch("/{category_id}", response_model=CategoryOut)
def update_category(category_id: str, body: CategoryUpdate, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> Category:
    cat = _get(db, user, category_id)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(cat, k, v)
    db.commit()
    return cat


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> Response:
    cat = _get(db, user, category_id)
    used = db.scalar(select(func.count()).select_from(Transaction)
                     .where(Transaction.user_id == user.id, Transaction.category_id == category_id))
    if used:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Category is used by {used} transactions")
    db.query(Budget).filter(Budget.user_id == user.id, Budget.category_id == category_id).delete()
    db.delete(cat)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
