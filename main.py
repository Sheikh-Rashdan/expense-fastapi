from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"about": "Expense API", "author": "Sheikh-Rashdan"}