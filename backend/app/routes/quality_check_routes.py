from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.quality_check import QualityCheck
from app.models.vehicle_production import VehicleProduction
from app.schemas.quality_check import (
    QualityCheckCreate,
    QualityCheckResponse,
    QualityCheckUpdate
)


router = APIRouter(
    prefix="/quality-checks",
    tags=["Quality Control System"]
)

quality_alias_router = APIRouter(
    tags=["Quality Control System"]
)


@router.post("/", response_model=QualityCheckResponse)
def create_quality_check(
    quality_check: QualityCheckCreate,
    db: Session = Depends(get_db)
):
    production = db.query(VehicleProduction).filter(
        VehicleProduction.id == quality_check.production_id
    ).first()

    if not production:
        raise HTTPException(
            status_code=404,
            detail="Production record not found"
        )

    new_quality_check = QualityCheck(**quality_check.model_dump())

    db.add(new_quality_check)
    db.commit()
    db.refresh(new_quality_check)

    return new_quality_check


@router.get("/", response_model=List[QualityCheckResponse])
def get_quality_checks(db: Session = Depends(get_db)):
    return db.query(QualityCheck).all()


@router.get("/production/{production_id}", response_model=List[QualityCheckResponse])
def get_production_quality_checks(
    production_id: int,
    db: Session = Depends(get_db)
):
    return db.query(QualityCheck).filter(
        QualityCheck.production_id == production_id
    ).all()


@router.get("/{quality_check_id}", response_model=QualityCheckResponse)
def get_single_quality_check(
    quality_check_id: int,
    db: Session = Depends(get_db)
):
    quality_check = db.query(QualityCheck).filter(
        QualityCheck.id == quality_check_id
    ).first()

    if not quality_check:
        raise HTTPException(
            status_code=404,
            detail="Quality check not found"
        )

    return quality_check


@router.put("/{quality_check_id}", response_model=QualityCheckResponse)
def update_quality_check(
    quality_check_id: int,
    quality_check_update: QualityCheckUpdate,
    db: Session = Depends(get_db)
):
    quality_check = db.query(QualityCheck).filter(
        QualityCheck.id == quality_check_id
    ).first()

    if not quality_check:
        raise HTTPException(
            status_code=404,
            detail="Quality check not found"
        )

    update_data = quality_check_update.model_dump(exclude_unset=True)

    if "production_id" in update_data:
        production = db.query(VehicleProduction).filter(
            VehicleProduction.id == update_data["production_id"]
        ).first()

        if not production:
            raise HTTPException(
                status_code=404,
                detail="Production record not found"
            )

    for key, value in update_data.items():
        setattr(quality_check, key, value)

    db.commit()
    db.refresh(quality_check)

    return quality_check


@router.delete("/{quality_check_id}")
def delete_quality_check(
    quality_check_id: int,
    db: Session = Depends(get_db)
):
    quality_check = db.query(QualityCheck).filter(
        QualityCheck.id == quality_check_id
    ).first()

    if not quality_check:
        raise HTTPException(
            status_code=404,
            detail="Quality check not found"
        )

    db.delete(quality_check)
    db.commit()

    return {
        "message": "Quality check deleted successfully"
    }


@quality_alias_router.post(
    "/quality-check",
    response_model=QualityCheckResponse
)
def create_quality_check_documented_endpoint(
    quality_check: QualityCheckCreate,
    db: Session = Depends(get_db)
):
    return create_quality_check(quality_check, db)


@quality_alias_router.get("/quality-report")
def get_quality_report(db: Session = Depends(get_db)):
    return {
        "total_checks": db.query(QualityCheck).count(),
        "passed": db.query(QualityCheck).filter(
            QualityCheck.quality_status == "passed"
        ).count(),
        "failed": db.query(QualityCheck).filter(
            QualityCheck.quality_status == "failed"
        ).count()
    }
