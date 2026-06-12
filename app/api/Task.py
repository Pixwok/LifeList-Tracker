from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.schemas import TaskResponse, CreateTask, ModifyTask
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
def create_task(task: CreateTask, db: Session = Depends(get_db)):
    data = Task(
        name=task.name, 
        description=task.description, 
        deadline=task.deadline, 
        objectif_id=task.objectif_id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return success_response(TaskResponse.model_validate(data))

# Modifier une tâche
@router.put("/{task_id}", response_model=APIResponse[TaskResponse])
def edit_task(task_id: int, task_edit: ModifyTask, db: Session = Depends(get_db)):
    task_row = db.query(Task).filter(Task.id == task_id).first()
    editfield = task_edit.model_dump(exclude_unset=True)
    
    for field, value in editfield.items():
        setattr(task_row, field, value)

    db.commit()
    db.refresh(task_row)    
    return success_response(TaskResponse.model_validate(task_row))

# Supprimer une tâche
@router.delete("/{task_id}", response_model=APIResponse[TaskResponse])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return success_response(TaskResponse.model_validate(task))