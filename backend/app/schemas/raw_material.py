from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class RawMaterialBase(BaseModel):
    material_code: str
    material_name: str
    stock_quantity: int
    unit_price: Decimal
    supplier_id: Optional[int] = None


class RawMaterialCreate(RawMaterialBase):
    pass


class RawMaterialUpdate(BaseModel):
    material_name: Optional[str] = None
    stock_quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    supplier_id: Optional[int] = None


class RawMaterialResponse(RawMaterialBase):
    id: int

    class Config:
        from_attributes = True