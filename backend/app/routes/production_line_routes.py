from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.production_line import ProductionLine
from app.models.department import Department

from app.schemas.production_line import (
    ProductionLineCreate,
    ProductionLineUpdate,
    ProductionLineResponse
)

router = APIRouter(
    prefix="/production-lines",
    tags=["Production Lines"]
)


@router.post("/", response_model=ProductionLineResponse)
def create_production_line(
    production_line: ProductionLineCreate,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == production_line.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    new_line = ProductionLine(
        **production_line.model_dump()
    )

    db.add(new_line)
    db.commit()
    db.refresh(new_line)

    return new_line


@router.get("/", response_model=List[ProductionLineResponse])
def get_production_lines(
    db: Session = Depends(get_db)
):
    return db.query(ProductionLine).all()


@router.get("/{line_id}", response_model=ProductionLineResponse)
def get_single_production_line(
    line_id: int,
    db: Session = Depends(get_db)
):
    line = db.query(ProductionLine).filter(
        ProductionLine.id == line_id
    ).first()

    if not line:
        raise HTTPException(
            status_code=404,
            detail="Production line not found"
        )

    return line


@router.put("/{line_id}", response_model=ProductionLineResponse)
def update_production_line(
    line_id: int,
    production_line_update: ProductionLineUpdate,
    db: Session = Depends(get_db)
):
    line = db.query(ProductionLine).filter(
        ProductionLine.id == line_id
    ).first()

    if not line:
        raise HTTPException(
            status_code=404,
            detail="Production line not found"
        )

    update_data = production_line_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(line, key, value)

    db.commit()
    db.refresh(line)

    return line


@router.delete("/{line_id}")
def delete_production_line(
    line_id: int,
    db: Session = Depends(get_db)
):
    line = db.query(ProductionLine).filter(
        ProductionLine.id == line_id
    ).first()

    if not line:
        raise HTTPException(
            status_code=404,
            detail="Production line not found"
        )

    db.delete(line)
    db.commit()

    return {
        "message": "Production line deleted successfully"
    }