from fastapi import FastAPI
from api.projects.router import router as projects_router
from api.users.router import router as users_router
from api.auth.router import router as auth_router
from database.database import create_tables

create_tables()

app = FastAPI()
app.include_router(projects_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

