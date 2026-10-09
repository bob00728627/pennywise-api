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
