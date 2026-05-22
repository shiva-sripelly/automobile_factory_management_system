from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    production_id = Column(
        Integer,
        ForeignKey("vehicle_production.id"),
        nullable=False
    )
    checked_by = Column(String, nullable=False)
    quality_status = Column(String, nullable=False)
    remarks = Column(String, nullable=True)

    production = relationship(
        "VehicleProduction",
        back_populates="quality_checks"
    )
