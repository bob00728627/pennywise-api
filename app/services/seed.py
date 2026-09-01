from sqlalchemy.orm import Session

from app.models import Category, User
from app.services.defaults import DEFAULT_CATEGORIES


def create_default_categories(db: Session, user: User) -> None:
    for c in DEFAULT_CATEGORIES:
        db.add(Category(user_id=user.id, **c))
