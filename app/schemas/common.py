from typing import Generic, Literal, TypeVar

from app.schemas.base import CamelModel

T = TypeVar("T")
TxType = Literal["income", "expense"]


class Page(CamelModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class Message(CamelModel):
    detail: str
