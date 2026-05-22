from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.models.inventory_transaction import (
    InventoryTransaction
)

from app.models.raw_material import RawMaterial

from app.schemas.inventory_transaction import (
    InventoryTransactionCreate,
    InventoryTransactionResponse
)

router = APIRouter(
    prefix="/inventory-transactions",
    tags=["Inventory Transactions"]
)


@router.post(
    "/",
    response_model=InventoryTransactionResponse
)
def create_inventory_transaction(
    transaction: InventoryTransactionCreate,
    db: Session = Depends(get_db)
):
    material = db.query(RawMaterial).filter(
        RawMaterial.id == transaction.material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Raw material not found"
        )

    if transaction.transaction_type == "IN":
        material.stock_quantity += transaction.quantity

    elif transaction.transaction_type == "OUT":

        if material.stock_quantity < transaction.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        material.stock_quantity -= transaction.quantity

    new_transaction = InventoryTransaction(
        **transaction.model_dump()
    )

    db.add(new_transaction)

    db.commit()

    db.refresh(new_transaction)

    return new_transaction


@router.get(
    "/",
    response_model=List[InventoryTransactionResponse]
)
def get_inventory_transactions(
    db: Session = Depends(get_db)
):
    return db.query(InventoryTransaction).all()