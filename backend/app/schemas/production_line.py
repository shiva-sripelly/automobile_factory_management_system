from pydantic import BaseModel
from typing import Optional


class ProductionLineBase(BaseModel):
    line_name: str
    department_id: int
    target_per_day: int
    current_output: Optional[int] = 0


class ProductionLineCreate(ProductionLineBase):
    pass


class ProductionLineUpdate(BaseModel):
    line_name: Optional[str] = None
    department_id: Optional[int] = None
    target_per_day: Optional[int] = None
    current_output: Optional[int] = None


class ProductionLineResponse(ProductionLineBase):
    id: int

    class Config:
        from_attributes = True