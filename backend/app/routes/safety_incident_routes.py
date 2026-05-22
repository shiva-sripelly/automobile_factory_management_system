from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.safety_incident import SafetyIncident
from app.models.worker import Worker
from app.schemas.safety_incident import (
    SafetyIncidentCreate,
    SafetyIncidentResponse,
    SafetyIncidentUpdate
)


router = APIRouter(
    prefix="/safety-incidents",
    tags=["Safety Incident Management"]
)


@router.post("/", response_model=SafetyIncidentResponse)
def create_safety_incident(
    incident: SafetyIncidentCreate,
    db: Session = Depends(get_db)
):
    worker = db.query(Worker).filter(
        Worker.id == incident.worker_id
    ).first()

    if not worker:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    new_incident = SafetyIncident(**incident.model_dump())

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get("/", response_model=List[SafetyIncidentResponse])
def get_safety_incidents(db: Session = Depends(get_db)):
    return db.query(SafetyIncident).all()


@router.get("/worker/{worker_id}", response_model=List[SafetyIncidentResponse])
def get_worker_safety_incidents(
    worker_id: int,
    db: Session = Depends(get_db)
):
    return db.query(SafetyIncident).filter(
        SafetyIncident.worker_id == worker_id
    ).all()


@router.get("/{incident_id}", response_model=SafetyIncidentResponse)
def get_single_safety_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(SafetyIncident).filter(
        SafetyIncident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Safety incident not found"
        )

    return incident


@router.put("/{incident_id}", response_model=SafetyIncidentResponse)
def update_safety_incident(
    incident_id: int,
    incident_update: SafetyIncidentUpdate,
    db: Session = Depends(get_db)
):
    incident = db.query(SafetyIncident).filter(
        SafetyIncident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Safety incident not found"
        )

    update_data = incident_update.model_dump(exclude_unset=True)

    if "worker_id" in update_data:
        worker = db.query(Worker).filter(
            Worker.id == update_data["worker_id"]
        ).first()

        if not worker:
            raise HTTPException(
                status_code=404,
                detail="Worker not found"
            )

    for key, value in update_data.items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)

    return incident


@router.delete("/{incident_id}")
def delete_safety_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(SafetyIncident).filter(
        SafetyIncident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Safety incident not found"
        )

    db.delete(incident)
    db.commit()

    return {
        "message": "Safety incident deleted successfully"
    }
