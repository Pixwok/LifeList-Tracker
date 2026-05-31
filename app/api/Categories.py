from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Categories).all()

@router.get("/{categorie_id}")
def get_category(categorie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Categories).filter(models.Categories.id == categorie_id).first()

@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    goal = models.Categories(name=name)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{categorie_id}")
def delete_category(categorie_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Categories).filter(models.Categories.id == categorie_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"Category Delete": category}