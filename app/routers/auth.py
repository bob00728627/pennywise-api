from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas.user import PasswordChange, Token, UserCreate, UserOut
from app.services.seed import create_default_categories, seed_demo_data

router = APIRouter(prefix="/api/auth", tags=["auth"])
