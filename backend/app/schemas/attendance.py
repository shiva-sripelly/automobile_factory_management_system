from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal
from typing import Optional


class AttendanceBase(BaseModel):
    worker_id: int
    attendance_date: date
    check_in: time
    check_out: Optional[time] = None
    overtime_hours: Optional[Decimal] = 0


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    overtime_hours: Optional[Decimal] = None


class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        from_attributes = True