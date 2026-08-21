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


class SettingsUpdate(CamelModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    currency: Literal["USD", "EUR", "GBP", "JPY", "INR", "CAD", "AUD"] | None = None
    theme: Literal["light", "dark"] | None = None


class PasswordChange(CamelModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class Token(CamelModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
