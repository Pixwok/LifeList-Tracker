# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from app.database import engine, Base
from app.api import Goals, Categories, Task
from app.api.response import error_response

app = FastAPI()

## Création des tables si n'existe pas
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

## Réponse erreur
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail).model_dump()
    )

## Router
app.include_router(Goals.router)
app.include_router(Categories.router)
app.include_router(Task.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")