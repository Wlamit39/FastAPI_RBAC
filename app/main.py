from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db
from app.api.v1 import auth, projects

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="RBAC API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)

@app.get("/")
def root():
    return {"message": "API is running successfully!"}
