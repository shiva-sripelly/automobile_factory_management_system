from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.worker import Worker
from app.models.department import Department
from app.schemas.worker import WorkerCreate, WorkerUpdate, WorkerResponse

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("", response_model=WorkerResponse)
@router.post("/", response_model=WorkerResponse)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == worker.department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    existing_worker = db.query(Worker).filter(
        Worker.employee_code == worker.employee_code
    ).first()

    if existing_worker:
        raise HTTPException(status_code=400, detail="Employee code already exists")

    new_worker = Worker(**worker.model_dump())
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    return new_worker


@router.get("", response_model=List[WorkerResponse])
@router.get("/", response_model=List[WorkerResponse])
def get_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()


@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    return worker


@router.put("/{worker_id}", response_model=WorkerResponse)
def update_worker(worker_id: int, worker_update: WorkerUpdate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    update_data = worker_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(worker, key, value)

    db.commit()
    db.refresh(worker)

    return worker


@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    db.delete(worker)
    db.commit()

    return {"message": "Worker deleted successfully"}
