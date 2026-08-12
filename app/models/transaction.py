from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(7))
    amount: Mapped[float] = mapped_column(Float)
    category_id: Mapped[str] = mapped_column(String(40), index=True)
    note: Mapped[str] = mapped_column(String(120), default="")
    date: Mapped[date] = mapped_column(Date, index=True)
    recurring: Mapped[bool] = mapped_column(Boolean, default=False)
