from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/goals", tags=["goals"])

# Récupère tout les objectifs
@router.get("/")
def list_goals(db: Session = Depends(get_db)):
    return db.query(models.Goals).all()

# Récupère un objectif
@router.get("/{goal_id}")
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goals).filter(models.Goals.id == goal_id).first()
    return goal

# Créer un objectif
@router.post("/")
def create_goal(name: str, categorie_id: int, db: Session = Depends(get_db)):
    goal = models.Goals(name=name, categorie_id=categorie_id)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

