from datetime import date as Date

from pydantic import Field

from app.schemas.base import CamelModel
from app.schemas.common import TxType


class TransactionBase(CamelModel):
    type: TxType
    amount: float = Field(gt=0, le=1_000_000_000)
    category_id: str
    note: str = Field(default="", max_length=120)
    date: Date
    recurring: bool = False


class TransactionCreate(TransactionBase):
    id: str | None = Field(default=None, max_length=40)


class TransactionUpdate(CamelModel):
    type: TxType | None = None
    amount: float | None = Field(default=None, gt=0, le=1_000_000_000)
    category_id: str | None = None
    note: str | None = Field(default=None, max_length=120)
    date: Date | None = None
    recurring: bool | None = None


class TransactionOut(TransactionBase):
    id: str


class BulkDelete(CamelModel):
    ids: list[str] = Field(min_length=1, max_length=1000)


class BulkResult(CamelModel):
    deleted: int
