from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.machinery import Machinery
from app.models.maintenance_log import MaintenanceLog
from app.models.robotics import Robotics
from app.schemas.maintenance_log import (
    MaintenanceLogCreate,
    MaintenanceLogUpdate,
    MaintenanceLogResponse
)


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("", response_model=MaintenanceLogResponse)
@router.post("/", response_model=MaintenanceLogResponse)
def create_maintenance_log(
    maintenance: MaintenanceLogCreate,
    db: Session = Depends(get_db)
):
    if not maintenance.machine_id and not maintenance.robot_id:
        raise HTTPException(
            status_code=400,
            detail="Either machine_id or robot_id is required"
        )

    if maintenance.robot_id:
        robot = db.query(Robotics).filter(
            Robotics.id == maintenance.robot_id
        ).first()

        if not robot:
            raise HTTPException(
                status_code=404,
                detail="Robot not found"
            )

    if maintenance.machine_id:
        machine = db.query(Machinery).filter(
            Machinery.id == maintenance.machine_id
        ).first()

        if not machine:
            raise HTTPException(
                status_code=404,
                detail="Machine not found"
            )

    new_log = MaintenanceLog(**maintenance.model_dump())

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


@router.get("", response_model=List[MaintenanceLogResponse])
@router.get("/", response_model=List[MaintenanceLogResponse])
def get_maintenance_logs(db: Session = Depends(get_db)):
    return db.query(MaintenanceLog).all()


@router.get("/cost-report")
def get_maintenance_cost_report(db: Session = Depends(get_db)):
    total_cost = db.query(
        func.coalesce(func.sum(MaintenanceLog.maintenance_cost), 0)
    ).scalar()

    total_logs = db.query(MaintenanceLog).count()

    return {
        "total_maintenance_logs": total_logs,
        "total_maintenance_cost": total_cost
    }


@router.get("/{maintenance_id}", response_model=MaintenanceLogResponse)
def get_single_maintenance_log(
    maintenance_id: int,
    db: Session = Depends(get_db)
):
    log = db.query(MaintenanceLog).filter(
        MaintenanceLog.id == maintenance_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Maintenance log not found"
        )

    return log


@router.put("/{maintenance_id}", response_model=MaintenanceLogResponse)
def update_maintenance_log(
    maintenance_id: int,
    maintenance_update: MaintenanceLogUpdate,
    db: Session = Depends(get_db)
):
    log = db.query(MaintenanceLog).filter(
        MaintenanceLog.id == maintenance_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Maintenance log not found"
        )

    update_data = maintenance_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(log, key, value)

    db.commit()
    db.refresh(log)

    return log


@router.delete("/{maintenance_id}")
def delete_maintenance_log(
    maintenance_id: int,
    db: Session = Depends(get_db)
):
    log = db.query(MaintenanceLog).filter(
        MaintenanceLog.id == maintenance_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Maintenance log not found"
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Maintenance log deleted successfully"
    }
