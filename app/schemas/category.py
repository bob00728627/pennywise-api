from pydantic import Field

from app.schemas.base import CamelModel
from app.schemas.common import TxType


class CategoryBase(CamelModel):
    name: str = Field(min_length=1, max_length=60)
    icon: str = Field(min_length=1, max_length=16)
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    type: TxType


class CategoryCreate(CategoryBase):
    id: str | None = Field(default=None, max_length=40)


class CategoryUpdate(CamelModel):
    name: str | None = Field(default=None, min_length=1, max_length=60)
    icon: str | None = Field(default=None, min_length=1, max_length=16)
    color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryOut(CategoryBase):
    id: str
