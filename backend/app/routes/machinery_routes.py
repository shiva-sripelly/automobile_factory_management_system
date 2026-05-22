from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.department import Department
from app.models.machinery import Machinery
from app.schemas.machinery import (
    MachineryCreate,
    MachineryResponse,
    MachineryUpdate
)


router = APIRouter(
    prefix="/machinery",
    tags=["Machinery Management"]
)


@router.post("", response_model=MachineryResponse)
@router.post("/", response_model=MachineryResponse)
def create_machine(
    machine: MachineryCreate,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == machine.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    existing_machine = db.query(Machinery).filter(
        Machinery.machine_code == machine.machine_code
    ).first()

    if existing_machine:
        raise HTTPException(
            status_code=400,
            detail="Machine code already exists"
        )

    new_machine = Machinery(**machine.model_dump())

    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)

    return new_machine


@router.get("", response_model=List[MachineryResponse])
@router.get("/", response_model=List[MachineryResponse])
def get_machines(db: Session = Depends(get_db)):
    return db.query(Machinery).all()


@router.get("/{machine_id}", response_model=MachineryResponse)
def get_machine(
    machine_id: int,
    db: Session = Depends(get_db)
):
    machine = db.query(Machinery).filter(
        Machinery.id == machine_id
    ).first()

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return machine


@router.put("/{machine_id}", response_model=MachineryResponse)
def update_machine(
    machine_id: int,
    machine_update: MachineryUpdate,
    db: Session = Depends(get_db)
):
    machine = db.query(Machinery).filter(
        Machinery.id == machine_id
    ).first()

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    update_data = machine_update.model_dump(exclude_unset=True)

    if "department_id" in update_data:
        department = db.query(Department).filter(
            Department.id == update_data["department_id"]
        ).first()

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    for key, value in update_data.items():
        setattr(machine, key, value)

    db.commit()
    db.refresh(machine)

    return machine


@router.delete("/{machine_id}")
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db)
):
    machine = db.query(Machinery).filter(
        Machinery.id == machine_id
    ).first()

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    db.delete(machine)
    db.commit()

    return {
        "message": "Machine deleted successfully"
    }
