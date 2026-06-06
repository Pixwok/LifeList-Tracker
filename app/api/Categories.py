from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/categories", tags=["categories"])

# Récupération des catégories
@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    data = db.query(models.Categories).all()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(data),
            "error": None,
        }
    )

# Récupérer une catégorie
@router.get("/{categorie_id}")
def get_category(categorie_id: int, db: Session = Depends(get_db)):
    data = db.query(models.Categories).filter(models.Categories.id == categorie_id).first()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(data),
            "error": None,
        }
    )

# Création catégorie
@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    data = models.Categories(name=name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(data),
            "error": None,
        }
    )

# Suppression catégorie
@router.delete("/{categorie_id}")
def delete_category(categorie_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Categories).filter(models.Categories.id == categorie_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return JSONResponse( 
        status_code=200,
        content={
            "success": True,
            "data": jsonable_encoder(category),
            "error": None,
        }
    )