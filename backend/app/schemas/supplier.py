from typing import Optional

from pydantic import BaseModel


class SupplierBase(BaseModel):
    supplier_name: str
    contact_person: str
    phone: str
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True
