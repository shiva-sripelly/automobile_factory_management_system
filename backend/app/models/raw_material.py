from sqlalchemy import Column, Integer, String, Numeric

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.database import Base


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    id = Column(Integer, primary_key=True, index=True)

    material_code = Column(String, unique=True, nullable=False)
    material_name = Column(String, nullable=False)

    stock_quantity = Column(Integer, default=0)

    unit_price = Column(Numeric(10, 2), nullable=False)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=True
    )

    supplier = relationship(
        "Supplier",
        back_populates="raw_materials"
    )

    inventory_transactions = relationship(
        "InventoryTransaction",
        back_populates="material"
    )
