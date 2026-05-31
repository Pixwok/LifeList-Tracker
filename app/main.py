# main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.models import *
from app.api import Goals

app = FastAPI()

## Création des tables si n'existe pas
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(Goals.router)