from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.robotics import Robotics
from app.models.department import Department
from app.schemas.robotics import (
    RoboticsCreate,
    RoboticsUpdate,
    RoboticsResponse
)


router = APIRouter(
    prefix="/robotics",
    tags=["Robotics"]
)


@router.post("", response_model=RoboticsResponse)
@router.post("/", response_model=RoboticsResponse)
def create_robot(
    robot: RoboticsCreate,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == robot.department_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    existing_robot = db.query(Robotics).filter(
        Robotics.robot_code == robot.robot_code
    ).first()

    if existing_robot:
        raise HTTPException(status_code=400, detail="Robot code already exists")

    new_robot = Robotics(**robot.model_dump())

    db.add(new_robot)
    db.commit()
    db.refresh(new_robot)

    return new_robot


@router.get("", response_model=List[RoboticsResponse])
@router.get("/", response_model=List[RoboticsResponse])
def get_robots(db: Session = Depends(get_db)):
    return db.query(Robotics).all()


@router.get("/{robot_id}", response_model=RoboticsResponse)
def get_robot(robot_id: int, db: Session = Depends(get_db)):
    robot = db.query(Robotics).filter(Robotics.id == robot_id).first()

    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")

    return robot


@router.put("/{robot_id}", response_model=RoboticsResponse)
def update_robot(
    robot_id: int,
    robot_update: RoboticsUpdate,
    db: Session = Depends(get_db)
):
    robot = db.query(Robotics).filter(Robotics.id == robot_id).first()

    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")

    update_data = robot_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(robot, key, value)

    db.commit()
    db.refresh(robot)

    return robot


@router.delete("/{robot_id}")
def delete_robot(robot_id: int, db: Session = Depends(get_db)):
    robot = db.query(Robotics).filter(Robotics.id == robot_id).first()

    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")

    db.delete(robot)
    db.commit()

    return {"message": "Robot deleted successfully"}
