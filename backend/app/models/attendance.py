from sqlalchemy import Column, Integer, Date, Time, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id"),
        nullable=False
    )

    attendance_date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=False)
    check_out = Column(Time, nullable=True)
    overtime_hours = Column(Numeric(5, 2), default=0)

    worker = relationship("Worker", back_populates="attendance_records")