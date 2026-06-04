# main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.api import Goals
from app.api import Categories

app = FastAPI()

## Création des tables si n'existe pas
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

## Router
app.include_router(Goals.router)
app.include_router(Categories.router)