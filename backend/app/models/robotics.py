from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Robotics(Base):
    __tablename__ = "robotics"

    id = Column(Integer, primary_key=True, index=True)
    robot_code = Column(String, unique=True, index=True, nullable=False)
    robot_name = Column(String, nullable=False)
    automation_type = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    maintenance_cycle_days = Column(Integer, nullable=False)
    current_status = Column(String, default="active")

    department = relationship("Department", back_populates="robotics")
    maintenance_logs = relationship("MaintenanceLog", back_populates="robot")