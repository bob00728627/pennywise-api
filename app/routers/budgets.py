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
