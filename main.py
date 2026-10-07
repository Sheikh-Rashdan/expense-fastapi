from fastapi import FastAPI
from database.db import initialize_db
from routers.user import user_router
from routers.category import category_router
from routers.expense import expense_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(expense_router)

@app.get("/")
def root():
    return {"about": "Expense API", "author": "Sheikh-Rashdan"}