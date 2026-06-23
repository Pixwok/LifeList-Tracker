from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Goals, Task
from app.schemas import GoalResponse, CreateGoal, ModifyGoal, TaskResponse
from app.api.response import APIResponse, success_response

router = APIRouter(prefix="/goals", tags=["goals"])

# Récupère tout les objectifs
@router.get("/", response_model=APIResponse[list[GoalResponse]])
def list_goals(db: Session = Depends(get_db)):
    data = db.query(Goals).all()
    return success_response([GoalResponse.model_validate(d) for d in data])

# Récupère un objectif
@router.get("/{goal_id}", response_model=APIResponse[GoalResponse])
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goals).filter(Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return success_response(GoalResponse.model_validate(goal))

# Récupérer les tâches d'un objectif
@router.get("/{goal_id}/task", response_model=APIResponse[list[TaskResponse]])
def getTaskForGoal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goals).filter(Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    tasks = db.query(Task).filter(Task.objectif_id == goal_id).all()
    return success_response([TaskResponse.model_validate(task) for task in tasks])

# Créer un objectif
@router.post("/", response_model=APIResponse[GoalResponse])
def create_goal(goal: CreateGoal, db: Session = Depends(get_db)):
    if db.query(Goals).filter(Goals.name == goal.name).first():
        raise HTTPException(status_code=404, detail="Goal name already exist")

    data = Goals(
        name=goal.name, 
        deadline=goal.deadline, 
        categorie_id=goal.categorie_id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return success_response(GoalResponse.model_validate(data))

# Modification objectif
@router.put("/{goal_id}", response_model=APIResponse[GoalResponse])
def edit_goal(goal_id: int, goal_edit: ModifyGoal, db: Session = Depends(get_db)):
    goal_row = db.query(Goals).filter(Goals.id == goal_id).first()

    if not goal_row:
        raise HTTPException(status_code=404, detail="Goal not found")
    if db.query(Goals).filter(Goals.name == goal_edit.name).first():
        raise HTTPException(status_code=404, detail="Goal name already exist")
    
    editfield = goal_edit.model_dump(exclude_unset=True)
    
    for field, value in editfield.items():
        setattr(goal_row, field, value)

    db.commit()
    db.refresh(goal_row)    
    return success_response(GoalResponse.model_validate(goal_row))

# Supprimer un objectifs
@router.delete("/{goal_id}", response_model=APIResponse[GoalResponse])
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goals).filter(Goals.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return success_response(GoalResponse.model_validate(goal))