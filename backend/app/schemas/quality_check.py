from typing import Optional

from pydantic import BaseModel


class QualityCheckBase(BaseModel):
    production_id: int
    checked_by: str
    quality_status: str
    remarks: Optional[str] = None


class QualityCheckCreate(QualityCheckBase):
    pass


class QualityCheckUpdate(BaseModel):
    production_id: Optional[int] = None
    checked_by: Optional[str] = None
    quality_status: Optional[str] = None
    remarks: Optional[str] = None


class QualityCheckResponse(QualityCheckBase):
    id: int

    class Config:
        from_attributes = True
