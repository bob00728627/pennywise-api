from typing import Literal

from pydantic import EmailStr, Field

from app.schemas.base import CamelModel


class UserCreate(CamelModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=8, max_length=128)
    seed_demo: bool = False


class UserOut(CamelModel):
    id: int
    email: EmailStr
    name: str
    currency: str
    theme: Literal["light", "dark"]
