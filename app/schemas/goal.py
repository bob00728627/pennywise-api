from datetime import date

from pydantic import Field

from app.schemas.base import CamelModel


class GoalBase(CamelModel):
    name: str = Field(min_length=1, max_length=80)
    target: float = Field(gt=0)
    saved: float = Field(default=0, ge=0)
    deadline: date
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")


class GoalCreate(GoalBase):
    id: str | None = None


class GoalUpdate(CamelModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    target: float | None = Field(default=None, gt=0)
    deadline: date | None = None
    color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class GoalOut(GoalBase):
    id: str
    percent: float = 0
    completed: bool = False
    days_left: int = 0
    monthly_needed: float = 0


class Deposit(CamelModel):
    amount: float = Field(description="Positive to deposit, negative to withdraw")
