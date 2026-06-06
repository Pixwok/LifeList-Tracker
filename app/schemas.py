from datetime import date
from pydantic import BaseModel

## Validation données catégorie
class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}  # Lecture depuis objet SQLAlchemy


class ModifyCategory(BaseModel):
    name: str

## Validation données objectifs
class GoalResponse(BaseModel):
    id: int
    name: str
    advancement: float
    statut: bool
    deadline: date | None
    categorie_id: int

    model_config = {"from_attributes": True}  # Lecture depuis objet SQLAlchemy


class ModifyGoal(BaseModel):
    name: str
    advancement: float = 0
    statut: bool = False
    deadline: date | None = None
    categorie_id: int 

## Validation données tâches
class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    statut: bool
    deadline: date | None
    objectif_id: int

    model_config = {"from_attributes": True}  # Lecture depuis objet SQLAlchemy

class ModifyTask(BaseModel):
    name: str
    description: str | None = None
    statut: bool = False
    deadline: date | None = None
    objectif_id: int