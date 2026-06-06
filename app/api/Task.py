from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.schemas import TaskResponse, ModifyTask
from app.api.response import APIResponse, success_response

router = APIRouter(prefix="/task", tags=["task"])

# Récupére les tâches
@router.get("/", response_model=APIResponse[list[TaskResponse]])
def list_tasks(limit: int = 10, db: Session = Depends(get_db)):
    data = db.query(Task).limit(limit).all()
    return success_response([TaskResponse.model_validate(d) for d in data])

# Récupère une tâche
@router.get("/{task_id}", response_model=APIResponse[TaskResponse])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(TaskResponse.model_validate(task))

# Créer une tâche
@router.post("/", response_model=APIResponse[TaskResponse])
def create_task(task: ModifyTask, db: Session = Depends(get_db)):
    task = Task(
        name=task.name, 
        description=task.description, 
        deadline=task.deadline, 
        objectif_id=task.objectif_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return success_response(TaskResponse.model_validate(task))