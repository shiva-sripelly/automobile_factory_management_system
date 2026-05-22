from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class PayrollBase(BaseModel):
    worker_id: int
    basic_salary: Decimal
    overtime_amount: Optional[Decimal] = 0
    deductions: Optional[Decimal] = 0
    final_salary: Decimal
    payment_status: Optional[str] = "pending"


class PayrollCreate(PayrollBase):
    pass


class PayrollUpdate(BaseModel):
    overtime_amount: Optional[Decimal] = None
    deductions: Optional[Decimal] = None
    final_salary: Optional[Decimal] = None
    payment_status: Optional[str] = None


class PayrollResponse(PayrollBase):
    id: int

    class Config:
        from_attributes = True