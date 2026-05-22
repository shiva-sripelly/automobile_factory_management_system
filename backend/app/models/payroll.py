from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id"),
        nullable=False
    )

    basic_salary = Column(
        Numeric(10, 2),
        nullable=False
    )

    overtime_amount = Column(
        Numeric(10, 2),
        default=0
    )

    deductions = Column(
        Numeric(10, 2),
        default=0
    )

    final_salary = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_status = Column(
        String,
        default="pending"
    )

    worker = relationship(
        "Worker",
        back_populates="payroll_records"
    )