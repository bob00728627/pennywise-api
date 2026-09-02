from datetime import date

from sqlalchemy.orm import Session

from app.core.ids import new_id
from app.models import Budget, Category, Goal, Transaction, User
from app.services.defaults import DEFAULT_CATEGORIES

NOTES = {
    "food": ["Groceries", "Ramen night", "Coffee", "Lunch with team", "Bakery"],
    "transport": ["Metro card", "Taxi", "Fuel", "Train ticket"],
    "shopping": ["New sneakers", "Books", "Headphones", "Home decor"],
    "health": ["Pharmacy", "Gym membership", "Dentist"],
    "fun": ["Cinema", "Concert tickets", "Streaming", "Board game"],
    "bills": ["Electricity", "Internet", "Phone plan", "Water"],
}


def create_default_categories(db: Session, user: User) -> None:
    for c in DEFAULT_CATEGORIES:
        db.add(Category(user_id=user.id, **c))


def seed_demo_data(db: Session, user: User, today: date | None = None) -> None:
    today = today or date.today()
    cats = list(NOTES)
    for back in range(5, -1, -1):
        y, m = today.year, today.month - back
        while m <= 0:
            y, m = y - 1, m + 12
        days = today.day if back == 0 else 28

        def day(d: int, y: int = y, m: int = m, days: int = days) -> date:
            return date(y, m, (d - 1) % days + 1)

        db.add(Transaction(id=new_id(), user_id=user.id, type="income", amount=4200, category_id="salary",
                           note="Monthly salary", date=day(1), recurring=True))
        db.add(Transaction(id=new_id(), user_id=user.id, type="expense", amount=1350, category_id="housing",
                           note="Rent", date=day(2), recurring=True))
        if back % 2 == 0:
            db.add(Transaction(id=new_id(), user_id=user.id, type="income", amount=600 + back * 90,
                               category_id="freelance", note="Client project", date=day(15)))
        for i in range(12):
            cat = cats[(i + back) % len(cats)]
            amount = round(12 + (i * 37 + back * 53) % 140, 2)
            notes = NOTES[cat]
            db.add(Transaction(id=new_id(), user_id=user.id, type="expense", amount=amount, category_id=cat,
                               note=notes[i % len(notes)], date=day(3 + i * 2)))
    for cat, limit in [("food", 400), ("shopping", 250), ("fun", 150), ("transport", 180)]:
        db.add(Budget(id=new_id(), user_id=user.id, category_id=cat, limit=limit))
    for name, target, saved, deadline, color in [
        ("Emergency fund", 10000, 6400, date(today.year + 1, 6, 30), "#22c55e"),
        ("Trip to Kyoto", 3000, 1150, date(today.year + 1, 3, 15), "#f97316"),
        ("New laptop", 2200, 1900, date(today.year + 1, 1, 10), "#6366f1"),
    ]:
        db.add(Goal(id=new_id(), user_id=user.id, name=name, target=target, saved=saved,
                    deadline=deadline, color=color))
