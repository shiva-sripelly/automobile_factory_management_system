from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class SafetyIncident(Base):
    __tablename__ = "safety_incidents"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    incident_type = Column(String, nullable=False)
    incident_date = Column(Date, nullable=False)
    severity = Column(String, nullable=False)
    remarks = Column(String, nullable=True)

    worker = relationship(
        "Worker",
        back_populates="safety_incidents"
    )
