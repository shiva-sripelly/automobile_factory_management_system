from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.role_checker import require_role

from app.schemas.factory_schema import FactoryCreate
from app.schemas.factory_schema import FactoryResponse
from app.schemas.factory_schema import FactoryUpdate

from app.services.factory_service import create_factory
from app.services.factory_service import delete_factory
from app.services.factory_service import get_factories
from app.services.factory_service import get_factory
from app.services.factory_service import update_factory


router = APIRouter(
    prefix="/factories",
    tags=["Factory Management"]
)


@router.post(
    "",
    response_model=FactoryResponse
)
def add_factory(
    factory: FactoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return create_factory(db, factory)


@router.get(
    "",
    response_model=list[FactoryResponse]
)
def list_factories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_factories(db)


@router.get(
    "/{factory_id}",
    response_model=FactoryResponse
)
def factory_details(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_factory(db, factory_id)


@router.put(
    "/{factory_id}",
    response_model=FactoryResponse
)
def edit_factory(
    factory_id: int,
    factory: FactoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return update_factory(db, factory_id, factory)


@router.delete("/{factory_id}")
def remove_factory(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return delete_factory(db, factory_id)
