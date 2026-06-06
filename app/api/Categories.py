from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Categories
from app.schemas import CategoryResponse, ModifyCategory
from app.api.response import APIResponse, success_response

router = APIRouter(prefix="/categories", tags=["categories"])

# Récupération des catégories
@router.get("/", response_model=APIResponse[list[CategoryResponse]])
def get_categories(db: Session = Depends(get_db)):
    data = db.query(Categories).all()
    return success_response([CategoryResponse.model_validate(d) for d in data])

# Récupérer une catégorie
@router.get("/{categorie_id}", response_model=APIResponse[CategoryResponse])
def get_category(categorie_id: int, db: Session = Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == categorie_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return success_response(CategoryResponse.model_validate(category))

# Création catégorie
@router.post("/", response_model=APIResponse[CategoryResponse])
def create_category(category: ModifyCategory, db: Session = Depends(get_db)):
    data = Categories(name=category.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return success_response(CategoryResponse.model_validate(data))

# Suppression catégorie
@router.delete("/{categorie_id}", response_model=APIResponse[CategoryResponse])
def delete_category(categorie_id: int, db: Session = Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == categorie_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return success_response(CategoryResponse.model_validate(category))