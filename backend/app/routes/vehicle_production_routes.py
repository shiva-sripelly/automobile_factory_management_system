from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.models.vehicle_production import (
    VehicleProduction
)

from app.models.production_line import (
    ProductionLine
)

from app.schemas.vehicle_production import (
    VehicleProductionCreate,
    VehicleProductionResponse
)

router = APIRouter(
    prefix="/vehicle-production",
    tags=["Vehicle Production"]
)

production_router = APIRouter(
    prefix="/production",
    tags=["Production"]
)


@router.post(
    "/",
    response_model=VehicleProductionResponse
)
def create_vehicle_production(
    vehicle: VehicleProductionCreate,
    db: Session = Depends(get_db)
):
    line = db.query(ProductionLine).filter(
        ProductionLine.id == vehicle.production_line_id
    ).first()

    if not line:
        raise HTTPException(
            status_code=404,
            detail="Production line not found"
        )

    new_vehicle = VehicleProduction(
        **vehicle.model_dump()
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


@router.get(
    "/",
    response_model=List[VehicleProductionResponse]
)
def get_vehicle_production(
    db: Session = Depends(get_db)
):
    return db.query(VehicleProduction).all()


@production_router.post(
    "",
    response_model=VehicleProductionResponse
)
@production_router.post(
    "/",
    response_model=VehicleProductionResponse
)
def create_production(
    vehicle: VehicleProductionCreate,
    db: Session = Depends(get_db)
):
    return create_vehicle_production(vehicle, db)


@production_router.get(
    "",
    response_model=List[VehicleProductionResponse]
)
@production_router.get(
    "/",
    response_model=List[VehicleProductionResponse]
)
def get_production(
    db: Session = Depends(get_db)
):
    return get_vehicle_production(db)


@production_router.get("/live-status")
def get_production_live_status(db: Session = Depends(get_db)):
    return {
        "production_lines": db.query(ProductionLine).all(),
        "total_production_records": db.query(VehicleProduction).count(),
        "completed": db.query(VehicleProduction).filter(
            VehicleProduction.completion_status == "completed"
        ).count(),
        "pending": db.query(VehicleProduction).filter(
            VehicleProduction.completion_status == "pending"
        ).count()
    }
