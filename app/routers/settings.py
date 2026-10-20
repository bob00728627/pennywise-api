from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import Budget, Category, Goal, Transaction, User
from app.schemas.backup import Backup, BackupSettings, GoalBackup
from app.schemas.budget import BudgetOut
from app.schemas.category import CategoryOut
from app.schemas.transaction import TransactionOut
from app.schemas.user import SettingsUpdate, UserOut
from app.services.seed import create_default_categories, seed_demo_data

router = APIRouter(prefix="/api", tags=["settings"])


def _wipe(db: Session, user: User, categories: bool = True) -> None:
    for model in (Transaction, Budget, Goal) + ((Category,) if categories else ()):
        db.execute(delete(model).where(model.user_id == user.id))


@router.patch("/settings", response_model=UserOut)
def update_settings(body: SettingsUpdate, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)) -> User:
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.commit()
    return user


@router.get("/backup", response_model=Backup)
def export_backup(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Backup:
    def rows(model):
        return db.scalars(select(model).where(model.user_id == user.id))

    return Backup(
        transactions=[TransactionOut.model_validate(t) for t in rows(Transaction)],
        categories=[CategoryOut.model_validate(c) for c in rows(Category)],
        budgets=[BudgetOut.model_validate(b) for b in rows(Budget)],
        goals=[GoalBackup.model_validate(g) for g in rows(Goal)],
        settings=BackupSettings(currency=user.currency, theme=user.theme, name=user.name),
    )


@router.post("/backup", response_model=Backup)
def import_backup(body: Backup, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Backup:
    """Replace all of the user's data with the uploaded backup (frontend JSON format)."""
    _wipe(db, user)
    db.flush()
    db.add_all(Category(user_id=user.id, **c.model_dump()) for c in body.categories)
    db.add_all(Transaction(user_id=user.id, **t.model_dump()) for t in body.transactions)
    db.add_all(Budget(user_id=user.id, **b.model_dump()) for b in body.budgets)
    db.add_all(Goal(user_id=user.id, **g.model_dump()) for g in body.goals)
    user.currency, user.theme, user.name = body.settings.currency, body.settings.theme, body.settings.name
    db.commit()
    return export_backup(user, db)


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset(demo: bool = True, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    """Clear everything. With demo=true, reload sample data."""
    _wipe(db, user)
    db.flush()
    create_default_categories(db, user)
    db.flush()
    if demo:
        seed_demo_data(db, user)
    db.commit()
