from app.schemas.base import CamelModel
from app.schemas.budget import BudgetOut
from app.schemas.category import CategoryOut
from app.schemas.goal import GoalBase
from app.schemas.transaction import TransactionOut


class GoalBackup(GoalBase):
    id: str


class BackupSettings(CamelModel):
    currency: str
    theme: str
    name: str


class Backup(CamelModel):
    """Same shape as the frontend's FinanceState so files are interchangeable."""

    transactions: list[TransactionOut]
    categories: list[CategoryOut]
    budgets: list[BudgetOut]
    goals: list[GoalBackup]
    settings: BackupSettings
