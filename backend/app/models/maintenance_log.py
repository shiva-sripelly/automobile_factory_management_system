from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(Integer, ForeignKey("machinery.id"), nullable=True)
    robot_id = Column(Integer, ForeignKey("robotics.id"), nullable=True)

    maintenance_type = Column(String, nullable=False)
    maintenance_cost = Column(Numeric(10, 2), nullable=False)
    maintenance_date = Column(Date, nullable=False)
    technician_name = Column(String, nullable=False)
    remarks = Column(String, nullable=True)

    robot = relationship("Robotics", back_populates="maintenance_logs")
    machine = relationship("Machinery", back_populates="maintenance_logs")