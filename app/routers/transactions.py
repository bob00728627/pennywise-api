import math
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.ids import new_id
from app.database import get_db
from app.models import Category, Transaction, User
from app.schemas.common import Page
from app.schemas.transaction import (
    BulkDelete,
    BulkResult,
    TransactionCreate,
    TransactionOut,
    TransactionUpdate,
)
from app.services.csv_export import transactions_to_csv

router = APIRouter(prefix="/api/transactions", tags=["transactions"])
