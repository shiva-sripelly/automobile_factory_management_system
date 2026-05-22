from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.factory import Factory

from app.schemas.factory_schema import FactoryCreate
from app.schemas.factory_schema import FactoryUpdate


def create_factory(
    db: Session,
    factory: FactoryCreate
):

    db_factory = Factory(
        factory_name=factory.factory_name,
        location=factory.location
    )

    db.add(db_factory)

    db.commit()

    db.refresh(db_factory)

    return db_factory


def get_factories(db: Session):

    return db.query(Factory).all()


def get_factory(
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

    return factory


def update_factory(
    db: Session,
    factory_id: int,
    factory: FactoryUpdate
):

    db_factory = get_factory(db, factory_id)

    update_data = factory.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_factory, field, value)

    db.commit()

    db.refresh(db_factory)

    return db_factory


def delete_factory(
    db: Session,
    factory_id: int
):

    db_factory = get_factory(db, factory_id)

    db.delete(db_factory)

    db.commit()

    return {
        "message": "Factory deleted successfully"
    }
