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
