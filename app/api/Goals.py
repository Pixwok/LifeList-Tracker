from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/goals", tags=["goals"])

# Récupère tout les objectifs
@router.get("/")
def list_goals(db: Session = Depends(get_db)):
    data = db.query(models.Goals).all()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(data),
            "error": None,
        }
    )

# Récupère un objectif
@router.get("/{goal_id}")
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goals).filter(models.Goals.id == goal_id).first()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(goal),
            "error": None,
        }
    )

# Créer un objectif
@router.post("/")
def create_goal(name: str, categorie_id: int, db: Session = Depends(get_db)):
    goal = models.Goals(name=name, categorie_id=categorie_id)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(goal),
            "error": None,
        }
    )

# Supprimer un objectifs
@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goals).filter(models.Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(goal),
            "error": None,
        }
    )