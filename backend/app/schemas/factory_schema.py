from datetime import datetime

from pydantic import BaseModel


class FactoryCreate(BaseModel):
    factory_name: str
    location: str


class FactoryUpdate(BaseModel):
    factory_name: str | None = None
    location: str | None = None


class FactoryResponse(BaseModel):
    id: int
    factory_name: str
    location: str
    total_departments: int
    created_at: datetime

    class Config:
        from_attributes = True
