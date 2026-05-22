from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.models.payroll import Payroll
from app.models.worker import Worker

from app.schemas.payroll import (
    PayrollCreate,
    PayrollUpdate,
    PayrollResponse
)

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"]
)


@router.post("/generate", response_model=PayrollResponse)
@router.post("/", response_model=PayrollResponse)
def create_payroll(
    payroll: PayrollCreate,
    db: Session = Depends(get_db)
):
    worker = db.query(Worker).filter(
        Worker.id == payroll.worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    new_payroll = Payroll(
        **payroll.model_dump()
    )

    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)

    return new_payroll


@router.get("", response_model=List[PayrollResponse])
@router.get("/", response_model=List[PayrollResponse])
def get_payroll_records(
    db: Session = Depends(get_db)
):
    return db.query(Payroll).all()


@router.get("/worker/{worker_id}", response_model=List[PayrollResponse])
def get_worker_payroll(
    worker_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Payroll).filter(
        Payroll.worker_id == worker_id
    ).all()


@router.get("/{payroll_id}", response_model=PayrollResponse)
def get_single_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found"
        )

    return payroll


@router.put("/{payroll_id}", response_model=PayrollResponse)
def update_payroll(
    payroll_id: int,
    payroll_update: PayrollUpdate,
    db: Session = Depends(get_db)
):
    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found"
        )

    update_data = payroll_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(payroll, key, value)

    db.commit()
    db.refresh(payroll)

    return payroll


@router.delete("/{payroll_id}")
def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    payroll = db.query(Payroll).filter(
        Payroll.id == payroll_id
    ).first()

    if not payroll:
        raise HTTPException(
            status_code=404,
            detail="Payroll record not found"
        )

    db.delete(payroll)
    db.commit()

    return {
        "message": "Payroll deleted successfully"
    }
