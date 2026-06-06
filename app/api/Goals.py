from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Goals
from app.schemas import GoalResponse, ModifyGoal
from app.api.response import APIResponse, success_response

router = APIRouter(prefix="/goals", tags=["goals"])

# Récupère tout les objectifs
@router.get("/", response_model=APIResponse[list[GoalResponse]])
def list_goals(limit: int = 10, db: Session = Depends(get_db)):
    data = db.query(Goals).limit(limit).all()
    return success_response([GoalResponse.model_validate(d) for d in data])

# Récupère un objectif
@router.get("/{goal_id}", response_model=APIResponse[GoalResponse])
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goals).filter(Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return success_response(GoalResponse.model_validate(goal))

# Créer un objectif
@router.post("/", response_model=APIResponse[GoalResponse])
def create_goal(goal: ModifyGoal, db: Session = Depends(get_db)):
    goal = Goals(
        name=goal.name, 
        deadline=goal.deadline, 
        categorie_id=goal.categorie_id
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return success_response(GoalResponse.model_validate(goal))

# Supprimer un objectifs
@router.delete("/{goal_id}", response_model=APIResponse[GoalResponse])
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goals).filter(Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return success_response(GoalResponse.model_validate(goal))