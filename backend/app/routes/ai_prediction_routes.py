from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.production_line import ProductionLine
from app.models.vehicle_production import VehicleProduction


router = APIRouter(
    prefix="/ai-production-prediction",
    tags=["AI Production Prediction"]
)


@router.get("/next-day")
def predict_next_day_production(db: Session = Depends(get_db)):
    production_lines = db.query(ProductionLine).all()
    predictions = []

    for line in production_lines:
        target = line.target_per_day or 0
        current_output = line.current_output or 0
        completion_ratio = current_output / target if target else 0
        predicted_output = int((current_output + target) / 2) if target else 0

        predictions.append({
            "production_line_id": line.id,
            "line_name": line.line_name,
            "target_per_day": target,
            "current_output": current_output,
            "completion_ratio": completion_ratio,
            "predicted_next_day_output": predicted_output
        })

    return {
        "model": "rule_based_baseline",
        "total_vehicle_records": db.query(VehicleProduction).count(),
        "predictions": predictions
    }
