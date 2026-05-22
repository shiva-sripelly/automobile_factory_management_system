from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class FactoryExpenseBase(BaseModel):
    expense_type: str
    amount: Decimal
    expense_date: date
    remarks: Optional[str] = None


class FactoryExpenseCreate(FactoryExpenseBase):
    pass


class FactoryExpenseUpdate(BaseModel):
    expense_type: Optional[str] = None
    amount: Optional[Decimal] = None
    expense_date: Optional[date] = None
    remarks: Optional[str] = None


class FactoryExpenseResponse(FactoryExpenseBase):
    id: int

    class Config:
        from_attributes = True
