from typing import Optional

from pydantic import BaseModel


class WarehouseBase(BaseModel):
    warehouse_name: str
    location: str
    capacity: int


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    warehouse_name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None


class WarehouseResponse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True
