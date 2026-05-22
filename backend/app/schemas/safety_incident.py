from datetime import date
from typing import Optional

from pydantic import BaseModel


class SafetyIncidentBase(BaseModel):
    worker_id: int
    incident_type: str
    incident_date: date
    severity: str
    remarks: Optional[str] = None


class SafetyIncidentCreate(SafetyIncidentBase):
    pass


class SafetyIncidentUpdate(BaseModel):
    worker_id: Optional[int] = None
    incident_type: Optional[str] = None
    incident_date: Optional[date] = None
    severity: Optional[str] = None
    remarks: Optional[str] = None


class SafetyIncidentResponse(SafetyIncidentBase):
    id: int

    class Config:
        from_attributes = True
