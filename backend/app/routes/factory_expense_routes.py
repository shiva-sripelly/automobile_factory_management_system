from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.factory_expense import FactoryExpense
from app.schemas.factory_expense import (
    FactoryExpenseCreate,
    FactoryExpenseResponse,
    FactoryExpenseUpdate
)


router = APIRouter(
    prefix="/factory-expenses",
    tags=["Cost & Expense Tracking"]
)

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Cost & Expense Tracking"]
)


@router.post("/", response_model=FactoryExpenseResponse)
def create_factory_expense(
    expense: FactoryExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = FactoryExpense(**expense.model_dump())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=List[FactoryExpenseResponse])
def get_factory_expenses(db: Session = Depends(get_db)):
    return db.query(FactoryExpense).all()


@router.get("/summary")
def get_factory_expense_summary(db: Session = Depends(get_db)):
    total_amount = db.query(
        func.coalesce(func.sum(FactoryExpense.amount), 0)
    ).scalar()

    total_expenses = db.query(FactoryExpense).count()

    return {
        "total_expenses": total_expenses,
        "total_amount": total_amount
    }


@router.get("/{expense_id}", response_model=FactoryExpenseResponse)
def get_single_factory_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    expense = db.query(FactoryExpense).filter(
        FactoryExpense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Factory expense not found"
        )

    return expense


@router.put("/{expense_id}", response_model=FactoryExpenseResponse)
def update_factory_expense(
    expense_id: int,
    expense_update: FactoryExpenseUpdate,
    db: Session = Depends(get_db)
):
    expense = db.query(FactoryExpense).filter(
        FactoryExpense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Factory expense not found"
        )

    update_data = expense_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}")
def delete_factory_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    expense = db.query(FactoryExpense).filter(
        FactoryExpense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Factory expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Factory expense deleted successfully"
    }


@expenses_router.post(
    "",
    response_model=FactoryExpenseResponse
)
@expenses_router.post(
    "/",
    response_model=FactoryExpenseResponse
)
def create_expense(
    expense: FactoryExpenseCreate,
    db: Session = Depends(get_db)
):
    return create_factory_expense(expense, db)


@expenses_router.get(
    "",
    response_model=List[FactoryExpenseResponse]
)
@expenses_router.get(
    "/",
    response_model=List[FactoryExpenseResponse]
)
def get_expenses(db: Session = Depends(get_db)):
    return get_factory_expenses(db)
