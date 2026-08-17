import hashlib
import hmac
import os
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import get_settings

ITERATIONS = 240_000
