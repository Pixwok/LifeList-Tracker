from datetime import date, datetime
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
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Lecture depuis objet SQLAlchemy

class CreateGoal(BaseModel):
    name: str
    advancement: float = 0
    statut: bool = False
    deadline: date | None = None
    categorie_id: int | None = None

class ModifyGoal(BaseModel):
    name: str | None = None
    advancement: float | None = None
    statut: bool | None = None
    deadline: date | None = None
    categorie_id: int | None = None

## Validation données tâches
class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    statut: bool
    deadline: date | None
    objectif_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Lecture depuis objet SQLAlchemy

class CreateTask(BaseModel):
    name: str
    description: str | None = None
    statut: bool = False 
    deadline: date | None = None
    objectif_id: int | None = None

class ModifyTask(BaseModel):
    name: str | None = None
    description: str | None = None
    statut: bool | None = None 
    deadline: date | None = None
    objectif_id: int | None = None