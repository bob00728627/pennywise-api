import math
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ids import new_id
from app.database import get_db
from app.models import Goal, User
from app.schemas.goal import Deposit, GoalCreate, GoalOut, GoalUpdate

router = APIRouter(prefix="/api/goals", tags=["goals"])


def to_out(g: Goal, today: date | None = None) -> GoalOut:
    today = today or date.today()
    pct = round(g.saved / g.target * 100, 1) if g.target else 0
    days = (g.deadline - today).days
    remaining = max(0.0, g.target - g.saved)
    months = max(1, math.ceil(days / 30)) if days > 0 else 1
    return GoalOut(id=g.id, name=g.name, target=g.target, saved=g.saved, deadline=g.deadline, color=g.color,
                   percent=pct, completed=g.saved >= g.target, days_left=days,
                   monthly_needed=round(remaining / months, 2) if days > 0 else remaining)
