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
