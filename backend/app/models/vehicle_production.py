from sqlalchemy import Column, Integer, String, Numeric, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class VehicleProduction(Base):
    __tablename__ = "vehicle_production"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_model = Column(String, nullable=False)

    production_line_id = Column(
        Integer,
        ForeignKey("production_lines.id"),
        nullable=False
    )

    chassis_number = Column(
        String,
        unique=True,
        nullable=False
    )

    production_stage = Column(String, nullable=False)

    completion_status = Column(String, default="pending")

    production_cost = Column(
        Numeric(12, 2),
        nullable=False
    )

    production_line = relationship(
        "ProductionLine"
    )

    quality_checks = relationship(
        "QualityCheck",
        back_populates="production",
        cascade="all, delete-orphan"
    )
