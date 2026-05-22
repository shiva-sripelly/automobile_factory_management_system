from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.machinery import Machinery
from app.models.robotics import Robotics


router = APIRouter(
    prefix="/iot-monitoring",
    tags=["IoT/Factory Monitoring Support"]
)


@router.get("/factory-status")
def get_factory_monitoring_status(db: Session = Depends(get_db)):
    total_running_hours = db.query(
        func.coalesce(func.sum(Machinery.running_hours), 0)
    ).scalar()

    return {
        "machinery": {
            "total": db.query(Machinery).count(),
            "active": db.query(Machinery).filter(
                Machinery.machine_status == "active"
            ).count(),
            "inactive": db.query(Machinery).filter(
                Machinery.machine_status != "active"
            ).count(),
            "total_running_hours": total_running_hours
        },
        "robotics": {
            "total": db.query(Robotics).count(),
            "active": db.query(Robotics).filter(
                Robotics.current_status == "active"
            ).count(),
            "inactive": db.query(Robotics).filter(
                Robotics.current_status != "active"
            ).count()
        }
    }


@router.get("/machine-health")
def get_machine_health_report(db: Session = Depends(get_db)):
    return db.query(Machinery).all()


@router.get("/robot-health")
def get_robot_health_report(db: Session = Depends(get_db)):
    return db.query(Robotics).all()
