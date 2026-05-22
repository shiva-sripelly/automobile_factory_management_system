from pydantic import BaseModel
from datetime import date


class InventoryTransactionBase(BaseModel):
    material_id: int
    transaction_type: str
    quantity: int
    transaction_date: date


class InventoryTransactionCreate(
    InventoryTransactionBase
):
    pass


class InventoryTransactionResponse(
    InventoryTransactionBase
):
    id: int

    class Config:
        from_attributes = True