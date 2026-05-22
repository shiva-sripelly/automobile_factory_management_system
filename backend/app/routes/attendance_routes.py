from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.attendance import Attendance
from app.models.worker import Worker
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    worker = db.query(Worker).filter(
        Worker.id == attendance.worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    existing_record = db.query(Attendance).filter(
        Attendance.worker_id == attendance.worker_id,
        Attendance.attendance_date == attendance.attendance_date
    ).first()

    if existing_record:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this worker today"
        )

    new_attendance = Attendance(
        **attendance.model_dump()
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@router.get("/", response_model=List[AttendanceResponse])
def get_attendance_records(
    db: Session = Depends(get_db)
):
    return db.query(Attendance).all()


@router.get("/worker/{worker_id}", response_model=List[AttendanceResponse])
def get_worker_attendance(
    worker_id: int,
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.worker_id == worker_id
    ).all()

    return records


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_single_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_update: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    update_data = attendance_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(attendance, key, value)

    db.commit()
    db.refresh(attendance)

    return attendance


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    db.delete(attendance)
    db.commit()

    return {
        "message": "Attendance record deleted successfully"
    }