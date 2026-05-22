from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Machinery(Base):
    __tablename__ = "machinery"

    id = Column(Integer, primary_key=True, index=True)
    machine_code = Column(String, unique=True, index=True, nullable=False)
    machine_name = Column(String, nullable=False)
    machine_type = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    purchase_date = Column(Date, nullable=False)
    warranty_expiry = Column(Date, nullable=False)
    machine_status = Column(String, default="active")
    running_hours = Column(Integer, default=0)

    department = relationship("Department", back_populates="machinery")
    maintenance_logs = relationship(
        "MaintenanceLog",
        back_populates="machine"
    )
