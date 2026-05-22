from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database import Base


class Factory(Base):

    __tablename__ = "factories"

    id = Column(Integer, primary_key=True, index=True)

    factory_name = Column(String, nullable=False)

    location = Column(String, nullable=False)

    total_departments = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    departments = relationship(
        "Department",
        back_populates="factory",
        cascade="all, delete-orphan"
    )
