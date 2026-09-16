import csv
import io

from app.models import Category, Transaction


def transactions_to_csv(txs: list[Transaction], categories: list[Category]) -> str:
    names = {c.id: c.name for c in categories}
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Date", "Type", "Category", "Amount", "Note"])
    for t in txs:
        writer.writerow([t.date.isoformat(), t.type, names.get(t.category_id, "Unknown"), f"{t.amount:.2f}", t.note])
    return buf.getvalue()
