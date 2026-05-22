from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database import Base

class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    department_name = Column(String, nullable=False)

    factory_id = Column(
        Integer,
        ForeignKey("factories.id"),
        nullable=False
    )
    workers = relationship("Worker", back_populates="department")
    factory = relationship("Factory", back_populates="departments")
    production_lines = relationship("ProductionLine", back_populates="department")   
    robotics = relationship("Robotics", back_populates="department")
    machinery = relationship("Machinery", back_populates="department")
