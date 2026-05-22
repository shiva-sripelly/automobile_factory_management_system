from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.models.raw_material import RawMaterial

from app.schemas.raw_material import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialResponse
)

router = APIRouter(
    prefix="/raw-materials",
    tags=["Raw Materials"]
)


@router.post("/", response_model=RawMaterialResponse)
def create_raw_material(
    material: RawMaterialCreate,
    db: Session = Depends(get_db)
):
    existing_material = db.query(RawMaterial).filter(
        RawMaterial.material_code == material.material_code
    ).first()

    if existing_material:
        raise HTTPException(
            status_code=400,
            detail="Material code already exists"
        )

    new_material = RawMaterial(
        **material.model_dump()
    )

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return new_material


@router.get("/", response_model=List[RawMaterialResponse])
def get_raw_materials(db: Session = Depends(get_db)):
    return db.query(RawMaterial).all()


@router.get("/{material_id}", response_model=RawMaterialResponse)
def get_raw_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(RawMaterial).filter(
        RawMaterial.id == material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Raw material not found"
        )

    return material


@router.put("/{material_id}", response_model=RawMaterialResponse)
def update_raw_material(
    material_id: int,
    material_update: RawMaterialUpdate,
    db: Session = Depends(get_db)
):
    material = db.query(RawMaterial).filter(
        RawMaterial.id == material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Raw material not found"
        )

    update_data = material_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(material, key, value)

    db.commit()
    db.refresh(material)

    return material


@router.delete("/{material_id}")
def delete_raw_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = db.query(RawMaterial).filter(
        RawMaterial.id == material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Raw material not found"
        )

    db.delete(material)
    db.commit()

    return {
        "message": "Raw material deleted successfully"
    }