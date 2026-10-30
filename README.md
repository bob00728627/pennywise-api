# 🪙 Pennywise API

REST backend for the [Pennywise](../pennywise) React frontend, built with
**FastAPI**, **SQLAlchemy 2** and **Pydantic v2**. JSON uses camelCase, so the
payloads match the frontend's TypeScript types one-to-one.

## ✨ Features

- **Auth** — register, OAuth2 password login with JWT bearer tokens, `/me`, change password. Passwords are hashed with salted PBKDF2-SHA256.
- **Categories** — per-user categories (10 defaults on sign-up), create / rename / recolor / delete (blocked while in use).
- **Transactions** — CRUD, search across notes and category names, filter by type, category and date range, sort by date or amount, pagination, bulk delete, CSV export.
- **Budgets** — one monthly limit per expense category with live `spent`, `remaining`, `percent`, `status` (`ok`/`warn`/`over`) and `perDayLeft`, for any month.
- **Goals** — savings goals with computed progress, days left and the monthly amount needed; deposit and withdraw.
- **Reports** — dashboard summary (balance, month income/expense, change vs last month, savings rate) and 3/6/12-month reports with monthly rows and category breakdown.
- **Settings & data** — name, currency and theme; full JSON backup export/import in the same format as the frontend; reset to empty or demo data.
- Every user's data is isolated; all routes except auth and health need a token.

## 🚀 Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive Swagger docs.

With Docker:

```bash
docker compose up --build
```

## 🧪 Tests and lint

```bash
pytest       # 44 tests
ruff check .
```

## 📚 Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/auth/register` | Create account (`seedDemo: true` loads sample data) |
| POST | `/api/auth/token` | Log in (form: `username`, `password`) |
| GET | `/api/auth/me` | Current user |
| POST | `/api/auth/password` | Change password |
| GET/POST | `/api/categories` | List (`?type=`) / create |
| PATCH/DELETE | `/api/categories/{id}` | Update / delete |
| GET/POST | `/api/transactions` | List with `q, type, categoryId, from, to, sort, page, pageSize` / create |
| GET/PATCH/DELETE | `/api/transactions/{id}` | Read / update / delete |
| POST | `/api/transactions/bulk-delete` | Delete many by id |
| GET | `/api/transactions/export.csv` | CSV export (same filters) |
| GET/PUT | `/api/budgets` | Status for `?month=YYYY-MM` / upsert by category |
| DELETE | `/api/budgets/{id}` | Delete budget |
| GET/POST | `/api/goals` | List / create |
| PATCH/DELETE | `/api/goals/{id}` | Update / delete |
| POST | `/api/goals/{id}/deposit` | Deposit (positive) or withdraw (negative) |
| GET | `/api/reports/summary` | Dashboard KPIs |
| GET | `/api/reports?months=6` | Report for 3, 6 or 12 months |
| PATCH | `/api/settings` | Update name, currency, theme |
| GET/POST | `/api/backup` | Export / import full backup |
| POST | `/api/reset?demo=true` | Reset data |
| GET | `/api/health` | Health check |
