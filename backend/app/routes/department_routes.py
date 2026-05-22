from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.role_checker import require_role

from app.schemas.department_schema import DepartmentCreate
from app.schemas.department_schema import DepartmentResponse
from app.schemas.department_schema import DepartmentUpdate

from app.services.department_service import create_department
from app.services.department_service import delete_department
from app.services.department_service import get_department
from app.services.department_service import get_departments
from app.services.department_service import get_factory_departments
from app.services.department_service import update_department


router = APIRouter(
    prefix="/departments",
    tags=["Department Management"]
)


@router.post(
    "",
    response_model=DepartmentResponse
)
def add_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return create_department(db, department)


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def list_departments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_departments(db)


@router.get(
    "/factory/{factory_id}",
    response_model=list[DepartmentResponse]
)
def list_factory_departments(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_factory_departments(db, factory_id)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def department_details(
    department_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_department(db, department_id)


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def edit_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return update_department(db, department_id, department)


@router.delete("/{department_id}")
def remove_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):

    return delete_department(db, department_id)
