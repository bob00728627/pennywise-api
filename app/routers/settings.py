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
