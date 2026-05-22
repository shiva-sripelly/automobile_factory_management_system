from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional

class WorkerBase(BaseModel):
    employee_code: str
    full_name: str
    department_id: int
    designation: str
    phone: Optional[str] = None
    address: Optional[str] = None
    joining_date: date
    salary: Decimal
    shift_type: str
    status: str = "active"

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(BaseModel):
    full_name: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    salary: Optional[Decimal] = None
    shift_type: Optional[str] = None
    status: Optional[str] = None

class WorkerResponse(WorkerBase):
    id: int

    class Config:
        from_attributes = True