from sqlalchemy import Column, Integer, String, Date, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)

    material_id = Column(
        Integer,
        ForeignKey("raw_materials.id"),
        nullable=False
    )

    transaction_type = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    transaction_date = Column(Date, nullable=False)

    material = relationship(
        "RawMaterial",
        back_populates="inventory_transactions"
    )