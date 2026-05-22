from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.factory import Factory

from app.schemas.department_schema import DepartmentCreate
from app.schemas.department_schema import DepartmentUpdate


def get_department(
    db: Session,
    department_id: int
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


def get_departments(db: Session):

    return db.query(Department).all()


def get_factory_departments(
    db: Session,
    factory_id: int
):

    factory = db.query(Factory).filter(
        Factory.id == factory_id
    ).first()

    if not factory:

        raise HTTPException(
            status_code=404,
            detail="Factory not found"
        )

    return db.query(Department).filter(
        Department.factory_id == factory_id
    ).all()


def create_department(
    db: Session,
    department: DepartmentCreate
):

    factory = db.query(Factory).filter(
        Factory.id == department.factory_id
    ).first()

    if not factory:

        raise HTTPException(
            status_code=404,
            detail="Factory not found"
        )

    db_department = Department(
        department_name=department.department_name,
        factory_id=department.factory_id
    )

    factory.total_departments += 1

    db.add(db_department)

    db.commit()

    db.refresh(db_department)

    return db_department


def update_department(
    db: Session,
    department_id: int,
    department: DepartmentUpdate
):

    db_department = get_department(db, department_id)

    update_data = department.model_dump(exclude_unset=True)

    new_factory_id = update_data.get("factory_id")

    if new_factory_id and new_factory_id != db_department.factory_id:

        old_factory = db.query(Factory).filter(
            Factory.id == db_department.factory_id
        ).first()

        new_factory = db.query(Factory).filter(
            Factory.id == new_factory_id
        ).first()

        if not new_factory:

            raise HTTPException(
                status_code=404,
                detail="Factory not found"
            )

        if old_factory and old_factory.total_departments > 0:
            old_factory.total_departments -= 1

        new_factory.total_departments += 1

    for field, value in update_data.items():
        setattr(db_department, field, value)

    db.commit()

    db.refresh(db_department)

    return db_department


def delete_department(
    db: Session,
    department_id: int
):

    db_department = get_department(db, department_id)

    factory = db.query(Factory).filter(
        Factory.id == db_department.factory_id
    ).first()

    if factory and factory.total_departments > 0:
        factory.total_departments -= 1

    db.delete(db_department)

    db.commit()

    return {
        "message": "Department deleted successfully"
    }
