from datetime import date
from typing import Optional

from pydantic import BaseModel


class MachineryBase(BaseModel):
    machine_code: str
    machine_name: str
    machine_type: str
    department_id: int
    purchase_date: date
    warranty_expiry: date
    machine_status: Optional[str] = "active"
    running_hours: Optional[int] = 0


class MachineryCreate(MachineryBase):
    pass


class MachineryUpdate(BaseModel):
    machine_name: Optional[str] = None
    machine_type: Optional[str] = None
    department_id: Optional[int] = None
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    machine_status: Optional[str] = None
    running_hours: Optional[int] = None


class MachineryResponse(MachineryBase):
    id: int

    class Config:
        from_attributes = True
