# Expense FastAPI

A lightweight FastAPI application for managing users, categories, and personal expenses with persistent SQLite storage, *built to learn FastAPI*.

## Features

- User management with create, read, update, and delete operations
- Category management linked to a specific user
- Expense tracking with filters for amount, date range, and category
- Per-user expense summary totals and category breakdown
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
│   └── models.py
├── models/
│   ├── category.py
│   ├── expense.py
│   ├── summary.py
│   └── user.py
├── routers/
│   ├── category.py
│   ├── expense.py
│   └── user.py
├── storage/
│   ├── category.py
│   ├── expense.py
│   └── user.py
├── main.py
├── pyproject.toml
├── uv.lock
├── database/
│   └── expenses.db
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
.venv\Scripts\activate
pip install -r requirements.txt
```

> This project uses `pyproject.toml` and `uv.lock`, so `uv sync` is the recommended setup path.

### Run the application

```bash
uv run uvicorn main:app --reload
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

### Users

```http
GET /users
POST /users
GET /users/{user_id}
PATCH /users/{user_id}
DELETE /users/{user_id}
GET /users/{user_id}/summary
```

### Categories

```http
GET /users/{user_id}/categories
POST /users/{user_id}/categories
GET /users/{user_id}/categories/{category_id}
PATCH /users/{user_id}/categories/{category_id}
DELETE /users/{user_id}/categories/{category_id}
```

### Expenses

```http
GET /users/{user_id}/expenses
POST /users/{user_id}/expenses
GET /users/{user_id}/expenses/{expense_id}
PATCH /users/{user_id}/expenses/{expense_id}
DELETE /users/{user_id}/expenses/{expense_id}
```

Expense listing supports filtering by:

- `min_amount`
- `max_amount`
- `start_date`
- `end_date`
- `category`
- `limit`
- `offset`

## Example Requests

Create a user:

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

Create a category:

```bash
curl -X POST "http://127.0.0.1:8000/users/1/categories" \
  -H "Content-Type: application/json" \
  -d '{"name": "Food"}'
```

Create an expense:

```bash
curl -X POST "http://127.0.0.1:8000/users/1/expenses" \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.5, "description": "Lunch", "date": "2026-10-08", "category_id": 1}'
```

Get a summary:

```bash
curl "http://127.0.0.1:8000/users/1/summary"
```

## Database

The app uses SQLite and creates the schema automatically on startup via SQLAlchemy model metadata.

Database file:

```text
database/expenses.db
```

## Future Improvements

The project is intentionally simple and suitable for learning FastAPI patterns, but it can be expanded in several useful directions:

- Add authentication and authorization with JWT or session-based login
- Restrict users so they can only access their own records and not other users' data
- Add monthly and yearly reporting dashboards for expenses
- Add CSV/Excel export for user expense data
- Add tests for routers, storage functions, and validation edge cases
- Add database migrations instead of creating tables directly on startup
- Add OpenAPI documentation enhancements and a production-ready security setup

## Notes

- Validation is implemented using FastAPI request models and dependency checks.
- User-owned categories and expenses are protected by ownership checks.
- Uniqueness and date-range validation are enforced in the router layer.
- The current project is a good foundation for adding authorization and stricter security patterns in a future iteration.
