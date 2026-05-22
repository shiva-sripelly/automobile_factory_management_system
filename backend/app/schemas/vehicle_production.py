from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class VehicleProductionBase(BaseModel):
    vehicle_model: str
    production_line_id: int
    chassis_number: str
    production_stage: str
    completion_status: Optional[str] = "pending"
    production_cost: Decimal


class VehicleProductionCreate(
    VehicleProductionBase
):
    pass


class VehicleProductionUpdate(BaseModel):
    production_stage: Optional[str] = None
    completion_status: Optional[str] = None
    production_cost: Optional[Decimal] = None


class VehicleProductionResponse(
    VehicleProductionBase
):
    id: int

    class Config:
        from_attributes = True