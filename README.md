# Expense FastAPI

A lightweight FastAPI application for managing users, categories, and personal expenses with persistent SQLite storage, *built to learn FastAPI*.

## Features

- User management with create, read, update, and delete operations
- Password-based login with bearer-token authentication
- Category management linked to a specific user
- Expense tracking with filters for amount, date range, and category
- Per-user expense summary totals and category breakdown
- Admin-only access to all users, categories, and expenses, plus admin-role management
- Automatic SQLite database initialization at startup

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- SQLite

## Project Structure

```text
expense-fastapi/
├── database/
│   ├── db.py
│   ├── models.py
│   └── expenses.db
├── models/
│   ├── category.py
│   ├── expense.py
│   ├── summary.py
│   └── user.py
├── routers/
│   ├── admin.py
│   ├── category.py
│   ├── expense.py
│   └── user.py
├── storage/
│   ├── category.py
│   ├── expense.py
│   └── user.py
├── utils/
│   └── security.py
├── .env.example
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.14+
- `uv` (recommended) or a standard virtual environment

### Install dependencies

Using `uv`:

```bash
uv sync
```

Or with a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi[standard] sqlalchemy bcrypt python-dotenv "python-jose[cryptography]"
```

> This project uses `pyproject.toml` and `uv.lock`, so `uv sync` is the recommended setup path.

### Configure the JWT secret

Copy `.env.example` to `.env` and replace the sample `JWT_KEY` value with a long, random secret before running the app. The key is used to sign access tokens.

### Run the application

With `uv`:

```bash
uv run uvicorn main:app --reload
```

With the virtual environment activated:

```bash
uvicorn main:app --reload
```

The app starts on the default FastAPI development server:

```text
http://127.0.0.1:8000
```

## API Overview

### Root

```http
GET /
```

Returns app metadata.

### Authentication

Creating a user requires `name`, `email`, and `password`. The first user created in an empty database is automatically made an admin. Log in with `POST /users/login` and use the returned `token` as a bearer token in the `Authorization` header for protected endpoints. Tokens expire after 30 minutes.

### Users

```http
POST /users
POST /users/login
GET /users/me
PATCH /users/me
DELETE /users/me
GET /users/me/summary
```

### Categories

```http
GET /categories
POST /categories
GET /categories/{category_id}
PATCH /categories/{category_id}
DELETE /categories/{category_id}
```

### Expenses

```http
GET /expenses
POST /expenses
GET /expenses/{expense_id}
PATCH /expenses/{expense_id}
DELETE /expenses/{expense_id}
```

Expense listing supports filtering by `min_amount`, `max_amount`, `start_date`, `end_date`, and `category_id`, as well as pagination with `limit` (maximum 100) and `offset`.

### Admin

All admin endpoints require a bearer token belonging to an admin user.

```http
GET /admin/users
GET /admin/categories
GET /admin/expenses
GET /admin/admins
PATCH /admin/admins/{user_id}
```

The list endpoints return records across all users and accept `limit` (default 100) and `offset` (default 0) query parameters. `PATCH /admin/admins/{user_id}` accepts a JSON body such as `{"is_admin": true}` to grant or remove admin privileges. Requests without a valid token receive `401`; authenticated non-admin users receive `403`.

## Example Requests

Create the first user (this user becomes an admin):

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "choose-a-password"}'
```

Log in to receive a bearer token:

```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "choose-a-password"}'
```

Use the returned token to create a category:

```bash
curl -X POST "http://127.0.0.1:8000/categories" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name": "Food"}'
```

Create an expense and retrieve your summary:

```bash
curl -X POST "http://127.0.0.1:8000/expenses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"amount": 25.5, "description": "Lunch", "date": "2026-10-08", "category_id": 1}'

curl "http://127.0.0.1:8000/users/me/summary" \
  -H "Authorization: Bearer <TOKEN>"
```

## Database

The app uses SQLite and creates the schema automatically on startup via SQLAlchemy model metadata. Passwords are stored as hashes; login tokens are signed using the `JWT_KEY` configured in `.env`.

Database file:

```text
database/expenses.db
```

## Future Improvements

The project is intentionally simple and suitable for learning FastAPI patterns, but it can be expanded in several useful directions:

- Add monthly and yearly reporting dashboards for expenses
- Add CSV/Excel export for user expense data
- Add tests for routers, storage functions, and validation edge cases
- Add database migrations instead of creating tables directly on startup
- Add OpenAPI documentation enhancements and strengthen the security setup for production

## Notes

- Validation is implemented using FastAPI request models and dependency checks.
- User-owned categories and expenses are protected by ownership checks; admin-wide endpoints require admin privileges.
- Uniqueness and date-range validation are enforced in the router layer.
- The current project is a learning-focused implementation and is not intended as a production-ready security solution.
