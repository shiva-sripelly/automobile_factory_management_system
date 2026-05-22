from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class ProductionLine(Base):
    __tablename__ = "production_lines"

    id = Column(Integer, primary_key=True, index=True)
    line_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    target_per_day = Column(Integer, nullable=False)
    current_output = Column(Integer, default=0)

    department = relationship(
        "Department",
        back_populates="production_lines"
    )