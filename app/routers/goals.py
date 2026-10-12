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


def _get(db: Session, user: User, goal_id: str) -> Goal:
    g = db.get(Goal, goal_id)
    if not g or g.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Goal not found")
    return g


@router.get("", response_model=list[GoalOut])
def list_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[GoalOut]:
    goals = db.scalars(select(Goal).where(Goal.user_id == user.id).order_by(Goal.deadline))
    return [to_out(g) for g in goals]


@router.post("", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(body: GoalCreate, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> GoalOut:
    g = Goal(user_id=user.id, **body.model_dump(exclude={"id"}), id=body.id or new_id())
    db.add(g)
    db.commit()
    return to_out(g)


@router.patch("/{goal_id}", response_model=GoalOut)
def update_goal(goal_id: str, body: GoalUpdate, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)) -> GoalOut:
    g = _get(db, user, goal_id)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(g, k, v)
    db.commit()
    return to_out(g)


@router.post("/{goal_id}/deposit", response_model=GoalOut)
def deposit(goal_id: str, body: Deposit, user: User = Depends(get_current_user),
            db: Session = Depends(get_db)) -> GoalOut:
    if body.amount == 0:
        raise HTTPException(422, "Amount must not be zero")
    g = _get(db, user, goal_id)
    g.saved = round(max(0.0, g.saved + body.amount), 2)
    db.commit()
    return to_out(g)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Response:
    db.delete(_get(db, user, goal_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
