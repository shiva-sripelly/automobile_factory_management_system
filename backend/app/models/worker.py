from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    designation = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    joining_date = Column(Date, nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    shift_type = Column(String, nullable=False)
    status = Column(String, default="active")

    department = relationship("Department", back_populates="workers")
    attendance_records = relationship("Attendance", back_populates="worker")
    payroll_records = relationship("Payroll", back_populates="worker")
    safety_incidents = relationship(
        "SafetyIncident",
        back_populates="worker",
        cascade="all, delete-orphan"
    )
