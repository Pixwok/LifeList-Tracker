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
    category_row = db.query(Categories).filter(Categories.name == category.name).first()
    if category_row:
        raise HTTPException(status_code=404, detail="Category already exist")
    data = Categories(name=category.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return success_response(CategoryResponse.model_validate(data))

# Mise à jour d'une catégorie
@router.put("/{categorie_id}", response_model=APIResponse[CategoryResponse])
def edit_goal(categorie_id: int, category_edit: ModifyCategory, db: Session = Depends(get_db)):
    category_row = db.query(Categories).filter(Categories.id == categorie_id).first()
    if not category_row:
        raise HTTPException(status_code=404, detail="Category not found")
    if db.query(Categories).filter(Categories.name == category_edit.name).first():
        raise HTTPException(status_code=404, detail="Category name already exist")
    editfield = category_edit.model_dump(exclude_unset=True)
    
    for field, value in editfield.items():
        setattr(category_row, field, value)

    db.commit()
    db.refresh(category_row)    
    return success_response(CategoryResponse.model_validate(category_row))

# Suppression catégorie
@router.delete("/{categorie_id}", response_model=APIResponse[CategoryResponse])
def delete_category(categorie_id: int, db: Session = Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == categorie_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return success_response(CategoryResponse.model_validate(category))