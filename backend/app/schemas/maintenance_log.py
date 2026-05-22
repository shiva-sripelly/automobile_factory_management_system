from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class MaintenanceLogBase(BaseModel):
    machine_id: Optional[int] = None
    robot_id: Optional[int] = None
    maintenance_type: str
    maintenance_cost: Decimal
    maintenance_date: date
    technician_name: str
    remarks: Optional[str] = None


class MaintenanceLogCreate(MaintenanceLogBase):
    pass


class MaintenanceLogUpdate(BaseModel):
    machine_id: Optional[int] = None
    robot_id: Optional[int] = None
    maintenance_type: Optional[str] = None
    maintenance_cost: Optional[Decimal] = None
    maintenance_date: Optional[date] = None
    technician_name: Optional[str] = None
    remarks: Optional[str] = None


class MaintenanceLogResponse(MaintenanceLogBase):
    id: int

    class Config:
        from_attributes = True