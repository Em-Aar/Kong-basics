from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from typing import Optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("user data services started")
    yield
    
app = FastAPI(lifespan = lifespan, title="user data services")

@app.get("/")
def root():
    return {"message": "Hello from user data services"}
